#!/usr/bin/env python3
"""
demo.py - A demonstration Python file showcasing various programming concepts

This file serves as a comprehensive example of Python programming patterns,
including data structures, functions, classes, file I/O, error handling,
and more.
"""

import os
import sys
import json
import datetime
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum


# ============================
# CONSTANTS AND CONFIGURATION
# ============================

CONFIG = {
    "app_name": "Demo Application",
    "version": "1.0.0",
    "debug": True,
    "max_items": 100
}


# ============================
# ENUMS AND DATA CLASSES
# ============================

class Status(Enum):
    """Enumeration for task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    """Data class representing a task."""
    id: int
    title: str
    description: str
    status: Status = Status.PENDING
    created_at: datetime.datetime = None
    
    def __post_init__(self):
        """Auto-set created_at if not provided."""
        if self.created_at is None:
            self.created_at = datetime.datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat()
        }


# ============================
# UTILITY FUNCTIONS
# ============================

def greet_user(name: str, title: str = "User") -> str:
    """
    Generate a personalized greeting message.
    
    Args:
        name: The user's name
        title: The user's title (default: "User")
    
    Returns:
        A formatted greeting string
    """
    return f"Hello, {title} {name}! Welcome to {CONFIG['app_name']} v{CONFIG['version']}."


def calculate_average(numbers: List[Union[int, float]]) -> float:
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers
    
    Returns:
        The average value
    
    Raises:
        ValueError: If the list is empty
    """
    if not numbers:
        raise ValueError("Cannot calculate average of empty list")
    return sum(numbers) / len(numbers)


def process_items(items: List[Dict]) -> List[Dict]:
    """
    Process a list of items by filtering and transforming them.
    
    Args:
        items: List of dictionaries with 'value' and 'active' keys
    
    Returns:
        Processed list of items
    """
    processed = []
    for item in items:
        if item.get("active", False) and item.get("value", 0) > 0:
            processed.append({
                "original": item["value"],
                "processed": item["value"] * 2,
                "timestamp": datetime.datetime.now().isoformat()
            })
    return processed[:CONFIG["max_items"]]


# ============================
# FILE OPERATIONS
# ============================

def save_data_to_file(filename: str, data: List[Dict]) -> bool:
    """
    Save data to a JSON file.
    
    Args:
        filename: Path to the output file
        data: List of dictionaries to save
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f"Error saving data to {filename}: {e}", file=sys.stderr)
        return False


def load_data_from_file(filename: str) -> Optional[List[Dict]]:
    """
    Load data from a JSON file.
    
    Args:
        filename: Path to the input file
    
    Returns:
        List of dictionaries or None if error
    """
    try:
        if not os.path.exists(filename):
            print(f"File not found: {filename}", file=sys.stderr)
            return None
        
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (IOError, OSError, json.JSONDecodeError) as e:
        print(f"Error loading data from {filename}: {e}", file=sys.stderr)
        return None


# ============================
# CLASS DEFINITIONS
# ============================

class TaskManager:
    """
    A class to manage tasks with CRUD operations.
    """
    
    def __init__(self, tasks: Optional[List[Task]] = None):
        """
        Initialize the task manager.
        
        Args:
            tasks: Optional list of initial tasks
        """
        self._tasks: List[Task] = tasks or []
        self._next_id = max([t.id for t in self._tasks], default=0) + 1
    
    def add_task(self, title: str, description: str) -> Task:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Task description
        
        Returns:
            The newly created task
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description
        )
        self._tasks.append(task)
        self._next_id += 1
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: The task ID
        
        Returns:
            The task or None if not found
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task_status(self, task_id: int, status: Status) -> bool:
        """
        Update a task's status.
        
        Args:
            task_id: The task ID
            status: The new status
        
        Returns:
            True if updated, False if task not found
        """
        task = self.get_task(task_id)
        if task:
            task.status = status
            return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.
        
        Args:
            task_id: The task ID
        
        Returns:
            True if deleted, False if task not found
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False
    
    def get_tasks_by_status(self, status: Status) -> List[Task]:
        """
        Get all tasks with a specific status.
        
        Args:
            status: The status to filter by
        
        Returns:
            List of tasks with the given status
        """
        return [task for task in self._tasks if task.status == status]
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks."""
        return self._tasks.copy()
    
    def to_dict(self) -> List[Dict]:
        """Convert all tasks to dictionaries."""
        return [task.to_dict() for task in self._tasks]


# ============================
# DECORATOR EXAMPLE
# ============================

def log_operation(func):
    """
    A decorator that logs function calls and their results.
    """
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Calling {func_name} with args={args}, kwargs={kwargs}")
        
        try:
            result = func(*args, **kwargs)
            print(f"[{timestamp}] {func_name} returned: {result}")
            return result
        except Exception as e:
            print(f"[{timestamp}] {func_name} raised: {e}")
            raise
    
    return wrapper


# ============================
# MAIN APPLICATION
# ============================

@log_operation
def main():
    """
    Main application entry point.
    Demonstrates all the features defined above.
    """
    print("=" * 60)
    print(f" {CONFIG['app_name']} v{CONFIG['version']} ")
    print("=" * 60)
    
    # Greeting
    print(greet_user("Developer", "Senior"))
    print()
    
    # Data processing example
    sample_items = [
        {"value": 10, "active": True},
        {"value": 20, "active": False},
        {"value": 30, "active": True},
        {"value": -5, "active": True},
        {"value": 40, "active": True},
    ]
    
    processed = process_items(sample_items)
    print(f"Processed {len(processed)} items:")
    for item in processed:
        print(f"  {item}")
    print()
    
    # File I/O example
    filename = "demo_output.json"
    if save_data_to_file(filename, processed):
        print(f"Data saved to {filename}")
        
        loaded_data = load_data_from_file(filename)
        if loaded_data:
            print(f"Loaded {len(loaded_data)} items from file")
    print()
    
    # Task manager example
    task_manager = TaskManager()
    task_manager.add_task("Learn Python", "Study advanced Python features")
    task_manager.add_task("Write code", "Write the demo application")
    task_manager.add_task("Review code", "Review the code for quality")
    
    task_manager.update_task_status(1, Status.IN_PROGRESS)
    task_manager.update_task_status(2, Status.COMPLETED)
    
    print("All tasks:")
    for task in task_manager.get_all_tasks():
        print(f"  [{task.status.value}] {task.title}: {task.description}")
    
    print(f"\nCompleted tasks: {len(task_manager.get_tasks_by_status(Status.COMPLETED))}")
    
    # Save tasks to file
    tasks_json = task_manager.to_dict()
    save_data_to_file("tasks.json", tasks_json)
    
    # Statistics example
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    try:
        avg = calculate_average(numbers)
        print(f"\nAverage of numbers: {avg:.2f}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print(" Demo completed successfully!")
    print("=" * 60)
    
    # Demonstrate cleanup
    # Delete the demo files
    try:
        os.remove(filename)
        os.remove("tasks.json")
        print("Cleaned up temporary files.")
    except OSError:
        pass


# ============================
# SCRIPT EXECUTION GUARD
# ============================

if __name__ == "__main__":
    main()