# import asyncio
# from typing import Callable, Coroutine, Optional
# from threading import Thread


#####################
# Reactor prototype #
#####################


# ##############
# # helpers.py #
# ##############

# # What are the limitations of this class?


# class ThrottledTasksExecutor:
#     def __init__(self, delay_between_tasks: float = 0.2, in_separate_process: bool = False):
#         self.loop = asyncio.new_event_loop()
#         self.running_tasks = set()  # TODO: Find the example with task removal from the set.
#                                     # TODO: Would be nice to have awaitable future, instead of infinite loop.
#         self.delay_between_tasks = 1
#         self.in_separate_process = in_separate_process

#         self.can_task_be_executed = asyncio.Condition(loop=self.loop)
#         self.is_running = False

#     def start(self, in_separate_process: Optional[bool] = None):
#         """Starts a thread (or a process), which executes coroutines provided to the ThrottledTasksExecutor"""
#         if in_separate_process is None:
#             in_separate_process = self.in_separate_process
#         # TODO: investigate a way to start coroutines in a separate process:
#         #   - https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor
#         # Param: in_separate_process: bool = False
#         thread = Thread(target=self._run_event_loop, daemon=True)
#         thread.start()

#         self.is_running = True

#         # Periodically emit permission to execute one task
#         asyncio.run_coroutine_threadsafe(self.allow_task_execution(every=self.delay_between_tasks), self.loop)

#     def stop(self):
#         """Terminates a thread (or a process), which executes coroutines provided to the ThrottledTasksExecutor"""
#         self.loop.stop()
#         self.is_running = False

#     def run(self, coroutine: Coroutine, callback: Callable):
#         """Executes coroutine in an executor thread, which makes sure not to hit throttling limits."""
#         # TODO: could add support for coroutines:
#         # if func is not coroutine and func is callable:
#         #     coroutine = func(*args, **kwargs)
#         #     if coroutine is not coroutine:
#         #         raise ValueError("Could not find coroutine")

#         # async with can_make_api_call:
#         #     task_result = task.result()

#         task = asyncio.run_coroutine_threadsafe(self.throttled_task(coroutine), self.loop)
#         self.running_tasks.add(task)
#         task.add_done_callback(self.mark_task_done(callback))

#     async def allow_task_execution(self, every: float, count: int = 1):
#         """Periodically emits event, which allows for one task to be executed."""
#         print("Started emitting execution events.")
#         while self.is_running:
#             print("Allowing one task execution.")
#             async with self.can_task_be_executed:   # TODO: is this async context really needed?
#                 self.can_task_be_executed.notify(n=count)
#             print("Allowed one task execution.")
#             await asyncio.sleep(every)
#         print("Stopped emitting execution events.")

#     def throttled_task(self, coroutine: Coroutine) -> Coroutine:
#         async def throttled_task_wrapper(*args, **kwargs):
#             async with self.can_task_be_executed:   # TODO: is this async context really needed?
#                 await self.can_task_be_executed.wait()
#             task_result = await coroutine
#             return task_result # task_result
#         return throttled_task_wrapper()

#     def mark_task_done(self, callback):
#         def task_done_wrapper(task):
#             task_result = task.result()
#             callback_result = callback(task_result)
#             self.running_tasks.discard(task)
#             return callback_result
#         return task_done_wrapper

#     def __enter__(self) -> "ThrottledTasksExecutor":
#         self.start()
#         return self

#     def __exit__(self, *exc_info):
#         asyncio.run(self.wait_for_tasks_to_finish())
#         self.stop()

#     async def wait_for_tasks_to_finish(self):
#         print(f"Started waiting for {len(self.running_tasks)} tasks to finish")
#         while self.running_tasks:
#             print(f"  Still waiting for {len(self.running_tasks)} tasks to finish")
#             await asyncio.sleep(0.3)

#     def _run_event_loop(self):
#         asyncio.set_event_loop(self.loop)
#         self.loop.run_forever()





# ## Plan:
# # Define task, which waits some time. And prints something.
# # Define function, which puts the tasks to be executed (multiple of them). 
#     # Test throtling: with diagram.
# # Execute some load testing on those functions.



# async def make_api_call(api_call_params) -> str:
#     # TODO: Can the task be a synchronous function?
#     # async with can_make_api_call:  # TODO: add this Condition
#     #     await can_make_api_call.wait()
#     print(f"{api_call_params} Making API call..")
#     await asyncio.sleep(2.4)
#     print(f"{api_call_params} Made API call..")
#     return str(api_call_params)


# def process_response(response: str):
#     print(f"Saving HTTP response with status code: {response}")
#     print(f"Finished processing the HTTP response {response}.") 
#     print(f"Removing the task from the pool of running tasks")


# ## TODO:
# # Implement that Condition.
# # Make real API calls using httpx.
# # Generalise the executor for different types of tasks: git clone and API calls.




# with ThrottledTasksExecutor(delay_between_tasks=0.2) as executor:
#     print("Creating the tasks:")
#     for api_call_params in range(10):
#         print(f"{api_call_params} Created task")
#         # TODO: I can put some arguments to the callback with functools.partial()
#         executor.run(make_api_call(api_call_params), callback=process_response)


#     # task = asyncio.run_coroutine_threadsafe(make_api_call(api_call_params), loop)
#     # running_tasks.add(task)
#     # print(f"Created task with id {api_call_params}")

#     # task.add_done_callback(process_http_response)


# #############
# ## Helpers ##
# #############





# print("All tasks have finished, exiting...")


# ## Problem:
# # Gather the dynamic set of tasks.
# # Should wait till all of the tasks are being finished.
# ## Solution:
# # Have a requirement that all of the tasks will be added before waiting happens.
# # Solution have a set of tasks, task has to remove itself from the running taskset when its done.
#     # Handle the case, when the task dies.


