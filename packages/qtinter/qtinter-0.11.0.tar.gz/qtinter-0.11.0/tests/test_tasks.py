from shim import QtCore
import asyncio
import inspect
import qtinter
import sys
import unittest


def print_stack():
    for i, o in enumerate(inspect.stack(0)):
        if i > 0:
            print(o)


def get_call_stack():
    return [o.function for o in inspect.stack(0)[1:]]


class TestRunTask(unittest.TestCase):
    # run_task should execute the task immediately until the first yield.

    def setUp(self) -> None:
        if QtCore.QCoreApplication.instance() is not None:
            self.app = QtCore.QCoreApplication.instance()
        else:
            self.app = QtCore.QCoreApplication([])
        self.loop = qtinter.QiDefaultEventLoop()

    def tearDown(self) -> None:
        self.loop.close()
        self.app = None

    def test_no_yield_benchmark(self):
        # create_task with coroutine with no yield is not executed eagerly
        async def coro(output):
            output.append(1)
            return 'finished'

        async def qi_test_entry():
            output = []
            task = self.loop.create_task(coro(output))
            self.assertFalse(task.done())
            self.assertEqual(output, [])
            value = await task
            self.assertEqual(output, [1])
            return value

        result = self.loop.run_until_complete(qi_test_entry())
        self.assertEqual(result, 'finished')

    def test_no_yield(self):
        # coroutine with no yield should be eagerly executed to completion
        async def coro():
            return get_call_stack()

        async def qi_test_entry():
            task = qtinter.run_task(coro())
            self.assertTrue(task.done())
            return task.result()

        result = self.loop.run_until_complete(qi_test_entry())
        self.assertIn('qi_test_entry', result)

    def test_one_yield(self):
        # coroutine with one yield should be eagerly executed
        async def coro(output):
            output.append(1)
            await asyncio.sleep(0)
            return get_call_stack()

        async def qi_test_entry():
            output = []
            task = qtinter.run_task(coro(output))
            self.assertEqual(output, [1])
            self.assertFalse(task.done())
            return await task

        result = self.loop.run_until_complete(qi_test_entry())
        self.assertNotIn('qi_test_entry', result)

    def test_interleaved(self):
        # run_task interleaved with create_task should work correctly
        var = 10

        async def coro1():
            nonlocal var
            var += 6
            await asyncio.sleep(0)
            var += 7

        async def coro2():
            nonlocal var
            var /= 8

        async def qi_test_entry():
            task2 = asyncio.create_task(coro2())
            task1 = qtinter.run_task(coro1())
            await asyncio.gather(task1, task2)

        self.loop.run_until_complete(qi_test_entry())
        self.assertEqual(var, 9)

    def test_current_task_before_yield(self):
        pass

    def test_current_task_after_yield(self):
        pass

    def test_current_task_before_yield_no_loop(self):
        pass

    def test_run_task_3(self):
        # running an async generator should raise an error (or not?)
        pass

    def test_raise_before_yield(self):
        # An exception raised before yield should be propagated to the caller
        pass

    def test_raise_after_yield(self):
        # Exceptions raised after yield should be treated normally
        pass

    def test_cancellation(self):
        # The returned task may be cancelled
        pass

    def test_nested(self):
        # run_task may run_task again, and still be immediate execution
        pass

    def test_recursive_ok(self):
        # run_task recursively
        pass

    def test_recursive_error(self):
        # run_task recursively too deeply should raise StackOverflowError
        pass

    @unittest.skipIf(sys.version_info < (3, 8), "requires Python >= 3.8")
    def test_task_name(self):
        # run_task should support task name.
        async def coro(output):
            output.append(1)
            await asyncio.sleep(0)

        async def entry():
            output = []
            task = qtinter.run_task(coro(output), name="MyTask!")
            self.assertEqual(task.get_name(), "MyTask!")
            self.assertEqual(output, [1])
            self.assertFalse(task.done())
            return await task

        self.loop.run_until_complete(entry())

    def test_disallow_nesting(self):
        # If task nesting is disabled, raise RuntimeError
        # run_task should support task name.
        async def coro():
            pass

        async def entry():
            qtinter.run_task(coro(), allow_task_nesting=False)

        with self.assertRaisesRegex(
                RuntimeError, "cannot call run_task from a running task"):
            self.loop.run_until_complete(entry())


class TestRunTaskWithoutRunningLoop(unittest.TestCase):

    def setUp(self) -> None:
        if QtCore.QCoreApplication.instance() is None:
            self.app = QtCore.QCoreApplication([])
        self.loop = qtinter.QiDefaultEventLoop()

    def tearDown(self) -> None:
        self.loop.close()

    # def test_no_yield_no_loop(self):
    #     # run_task with no yield and no running loop should be ok
    #     async def coro():
    #         return 'magic'
    #
    #     task = self.loop.run_task(coro())
    #     self.assertTrue(task.done())
    #     self.assertEqual(task.result(), 'magic')

    # def test_one_yield_no_loop(self):
    #     # run_task with no running loop should still execute the first step.
    #     state = 'initial'
    #
    #     async def coro():
    #         nonlocal state
    #         state = 'executed'
    #         await asyncio.sleep(0)
    #         state = 'finished'
    #
    #     task = self.loop.run_task(coro())
    #     self.assertEqual(state, 'executed')
    #     self.assertFalse(task.done())
    #     # Finish the suspended task
    #     self.loop.run_until_complete(task)
    #     self.assertTrue(task.done())
    #     self.assertEqual(state, 'finished')


if __name__ == '__main__':
    unittest.main()
