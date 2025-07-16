import uuid
import json
import os
from tool_registry import call_tool

class TaskManager:
    """
    TaskManager handles task generation, prioritization, execution, feedback, logging, and pluggable tool use.
    If the LLM result contains 'TOOL: tool_name: arg', the tool is called and its output appended to the result.
    """
    def __init__(self, llm, vector_store, max_tasks=10, log_file='output.log', results_file='results.json'):
        self.llm = llm
        self.vector_store = vector_store
        self.max_tasks = max_tasks
        self.tasks = []
        self.completed = []  # List of dicts: {task, result}
        self.memory = []     # Store all results for context
        self.log_file = log_file
        self.results_file = results_file
        if os.path.exists(self.results_file):
            with open(self.results_file, 'r') as f:
                self.completed = json.load(f)
                self.memory = self.completed.copy()

    def log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')

    def save_results(self):
        with open(self.results_file, 'w') as f:
            json.dump(self.completed, f, indent=2)

    def generate_tasks(self, objective):
        context = "\n".join([f"Task: {item['task']}\nResult: {item['result']}" for item in self.memory[-5:]])
        prompt = f"Objective: {objective}\n"
        if context:
            prompt += f"Previous results (for context):\n{context}\n"
        prompt += "Generate a list of tasks to achieve the objective, considering the above context."
        tasks_text = self.llm.generate(prompt)
        self.tasks = [t.strip() for t in tasks_text.split('\n') if t.strip()][:self.max_tasks]
        self.log(f"[GENERATE_TASKS] Objective: {objective}\nPrompt: {prompt}\nTasks: {self.tasks}")

    def prioritize_tasks(self):
        self.tasks = self.tasks[:self.max_tasks]
        self.log(f"[PRIORITIZE_TASKS] Tasks: {self.tasks}")

    def execute_task(self, task):
        prompt = f"Execute the following task: {task}"
        result = self.llm.generate(prompt)
        # Tool use: check for TOOL: tool_name: arg
        if result.strip().startswith('TOOL:'):
            try:
                _, tool_name, tool_arg = result.strip().split(':', 2)
                tool_name = tool_name.strip()
                tool_arg = tool_arg.strip()
                tool_output = call_tool(tool_name, tool_arg)
                result += f"\n[TOOL_OUTPUT] {tool_output}"
                self.log(f"[TOOL_USE] {tool_name}({tool_arg}) => {tool_output}")
            except Exception as e:
                result += f"\n[TOOL_ERROR] {e}"
                self.log(f"[TOOL_ERROR] {e}")
        embedding = [0.0] * 1536
        self.vector_store.add_task(str(uuid.uuid4()), embedding, {"task": task, "result": result})
        record = {"task": task, "result": result}
        self.completed.append(record)
        self.memory.append(record)
        self.log(f"[EXECUTE_TASK] Task: {task}\nResult: {result}")
        print(f"[INFO] Executing: {task}\n[OUTPUT] {result}")
        feedback_prompt = (
            f"Reflect on the result of the following task and suggest improvements or follow-up tasks.\n"
            f"Task: {task}\nResult: {result}\n"
            f"If improvements or follow-ups are needed, list them as new tasks. Otherwise, reply 'No further action needed.'"
        )
        feedback = self.llm.generate(feedback_prompt)
        self.log(f"[FEEDBACK] {feedback}")
        print(f"[FEEDBACK] {feedback}")
        if 'No further action needed' not in feedback:
            new_tasks = [t.strip() for t in feedback.split('\n') if t.strip()]
            self.tasks.extend(new_tasks)
            self.prioritize_tasks()
        self.save_results()

    def run_loop(self, objective):
        self.generate_tasks(objective)
        self.prioritize_tasks()
        while self.tasks:
            task = self.tasks.pop(0)
            print(f"\n[INTERACTIVE] Next task: {task}")
            print("Options: [a]pprove, [e]dit, [s]kip, [n]ew task, [c]hange objective, [q]uit")
            choice = input("Your choice: ").strip().lower()
            self.log(f"[USER_CHOICE] Task: {task} Choice: {choice}")
            if choice == 'a' or choice == '':
                self.execute_task(task)
            elif choice == 'e':
                new_task = input("Edit task: ").strip()
                if new_task:
                    self.execute_task(new_task)
            elif choice == 's':
                print("[INFO] Task skipped.")
                self.log(f"[SKIP_TASK] {task}")
                continue
            elif choice == 'n':
                new_task = input("Enter new task: ").strip()
                if new_task:
                    self.tasks.insert(0, new_task)
                    self.log(f"[NEW_TASK] {new_task}")
            elif choice == 'c':
                new_objective = input("Enter new objective: ").strip()
                if new_objective:
                    self.log(f"[CHANGE_OBJECTIVE] {new_objective}")
                    self.generate_tasks(new_objective)
                    self.prioritize_tasks()
                    continue
            elif choice == 'q':
                print("[INFO] Exiting agent loop.")
                self.log("[QUIT]")
                break
            else:
                print("[WARN] Invalid choice. Approving by default.")
                self.log(f"[INVALID_CHOICE] {choice} for task {task}")
                self.execute_task(task) 