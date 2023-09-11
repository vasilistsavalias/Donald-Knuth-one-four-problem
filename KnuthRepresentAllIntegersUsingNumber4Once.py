import tkinter as tk
from tkinter import messagebox
import math
import time

result = 0
operations_window = 0


def apply_ops(num):
    floor_num = math.floor(num)
    sqrt_num = math.sqrt(num)

    if num <= 170:
        factorial_num = math.factorial(int(num))
    else:
        factorial_num = None

    return floor_num, sqrt_num, factorial_num


class Node:
    def __init__(self, value, parent=None, operation=None):
        self.value = value
        self.parent = parent
        self.operation = operation
        self.children = []

    def generate_children(self):
        floor_num, sqrt_num, factorial_num = apply_ops(self.value)
        if floor_num is not None:
            self.children.append(Node(floor_num, self, "floor"))
        if sqrt_num is not None:
            self.children.append(Node(sqrt_num, self, "sqrt"))
        if factorial_num is not None:
            self.children.append(Node(factorial_num, self, "factorial"))


def bfs(start, goal):
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node.value == goal:
            return node
        node.generate_children()
        queue.extend(node.children)
    return None


def iddfs(start, goal, max_depth):
    for depth in range(max_depth):
        result = dfs_with_depth_limit(start, goal, depth)
        if result is not None:
            return result
    return None


def dfs_with_depth_limit(node, goal, depth_limit):
    if depth_limit == 0 and node.value == goal:
        return node
    if depth_limit > 0:
        node.generate_children()
        for child in node.children:
            result = dfs_with_depth_limit(child, goal, depth_limit - 1)
            if result is not None:
                return result
    return None


def calculate():

    operations_window = tk.Toplevel(window)
    operations_window.title("Operations Used")

    global operations_text
    operations_text = tk.Text(operations_window)
    operations_text.pack()
    goal = goal_entry.get()
    if not goal.isdigit():
        messagebox.showerror("Error", "Please enter a positive integer.")
        return

    goal = int(goal)
    algo_type = algo_var.get()
    start_node = Node(4)
    same_goal = (start_node.value == goal)

    start_time = time.time()

    if algo_type == "BFS":
        result = bfs(start_node, goal)
    else:
        result = iddfs(start_node, goal, 1000)

    end_time = time.time()
    elapsed_time = end_time - start_time

    operations_text.bind("<Configure>", adjust_operations_window_size)

    if result is not None:
        result_label.config(text=f"The shortest path from 4 to {goal} is:")
        if same_goal:
            path_label.config(
                text="We don't need to do any operations, thus the path is empty")
        else:
            path = []
            while result is not None:
                if result.operation is None:
                    break
                path.append(result.operation)
                result = result.parent
            path = path[::-1]
            path_str = "\n".join(
                [f"Step {i + 1}: {op}" for i, op in enumerate(path)])
            path_label.config(text=path_str)
            show_operations_button.config(state="normal")
    else:
        result_label.config(text="No solution found")
    time_label.config(
        text=f"By using the {algo_type} implementation, we needed {elapsed_time:.2f} seconds to complete the calculation.")


def adjust_operations_window_size(event=None):
    text_height = operations_text.count("1.0", tk.END, "lines")
    operations_window.geometry(f"400x{40 + text_height * 15}")

    # Initial size


# Create the tkinter window
window = tk.Tk()
window.title("Shortest Path Calculator")

# Calculate the screen width and height for centering
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window_width = 400
window_height = 900
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Add widgets
goal_label = tk.Label(window, text="Enter a positive integer:")
goal_label.pack()

goal_entry = tk.Entry(window)
goal_entry.pack()

algo_label = tk.Label(window, text="Choose the algorithm implementation:")
algo_label.pack()

algo_var = tk.StringVar()
algo_var.set("BFS")

bfs_radio = tk.Radiobutton(
    window, text="Breadth-First Search (BFS)", variable=algo_var, value="BFS")
bfs_radio.pack()

iddfs_radio = tk.Radiobutton(
    window, text="Iterative Deepening Depth-First Search (IDDFS)", variable=algo_var, value="IDDFS")
iddfs_radio.pack()

calculate_button = tk.Button(window, text="Calculate", command=calculate)
calculate_button.pack()

result_label = tk.Label(window, text="")
result_label.pack()

path_label = tk.Label(window, text="")
path_label.pack()


time_label = tk.Label(window, text="")
time_label.pack()

# Start the tkinter main loop
window.mainloop()
