.. currentmodule:: qtinter

API Reference
=============

:mod:`qtinter` provides the following functions and classes in its
public API:

`Context managers`_ for asyncio-Qt interop:

* :func:`using_asyncio_from_qt` enables Qt-driven code
  to use asyncio-based components.

* :func:`using_qt_from_asyncio` enables asyncio-driven code
  to use Qt-based components.


`Helper functions`_ to make interp code fit naturally into the
current coding pattern:

* :func:`asyncsignal` makes a Qt signal *awaitable*;
  useful for asyncio-driven code.

* :func:`asyncsignalstream` exposes a Qt signal as an asynchronous
  iterator; useful for asyncio-driven code.

* :func:`asyncslot` connects a coroutine function
  to a Qt signal; useful for Qt-driven code.

* :func:`modal` allows the asyncio event loop to continue running
  in a nested Qt event loop.

* :func:`multisignal` collects multiple Qt signals and re-emits
  them with a tag.

* :func:`run_task` creates an :class:`asyncio.Task` and eagerly
  executes its first step.


`Loop factory`_ to create `event loop objects`_ directly:

* :func:`new_event_loop` creates an asyncio-compatible *logical*
  event loop object that runs on top of a *physical* Qt event loop.


`Low-level classes`_ that do the actual work of bridging Qt and asyncio:

* `Event loop interface`_

* `Event loop objects`_

* `Event loop policy objects`_


`Private API`_ that supports the internal implementation of :mod:`qtinter`.


Context managers
----------------

.. function:: using_asyncio_from_qt()

   Context manager that enables enclosed *Qt-driven* code to use
   asyncio-based libraries.

   Your code is *Qt-driven* if it calls ``app.exec()`` or equivalent
   as its entry point.

   Example:

   .. code-block:: python

      app = QtWidgets.QApplication([])
      with qtinter.using_asyncio_from_qt():
          app.exec()
   
.. function:: using_qt_from_asyncio()

   Context manager that enables enclosed *asyncio-driven* code to use
   Qt components.

   Your code is *asyncio-driven* if it calls :func:`asyncio.run()` or
   equivalent as its entry point.

   .. note::

      This context manager modifies the global (per-interpreter) asyncio
      event loop policy.  Do not use this context manager if your code
      uses event loops from multiple threads.
      Instead, call :func:`new_event_loop` to create an
      event loop object and call its methods directly.
      Since Python 3.11, use :class:`asyncio.Runner` and pass
      :class:`new_event_loop` as its *loop_factory* parameter.
      

Helper functions
----------------

.. function:: asyncsignal(signal: BoundSignal[typing.Unpack[Ts]]) -> typing.Tuple[typing.Unpack[Ts]]
   :async:

   Wait for *signal* to emit and return the emitted arguments in a
   :class:`tuple`.

   .. _PyQt5.QtCore.pyqtSignal: https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html#PyQt5.QtCore.pyqtSignal
   .. _PyQt6.QtCore.pyqtSignal: https://www.riverbankcomputing.com/static/Docs/PyQt6/signals_slots.html#PyQt6.QtCore.pyqtSignal
   .. _PySide2.QtCore.Signal: https://doc.qt.io/qtforpython-5/PySide2/QtCore/Signal.html
   .. _PySide6.QtCore.Signal: https://doc.qt.io/qtforpython/PySide6/QtCore/Signal.html#PySide6.QtCore.PySide6.QtCore.Signal

   .. _AutoConnection: https://doc.qt.io/qt-6/qt.html#ConnectionType-enum

   *signal* must be a bound Qt signal object, i.e. a bound
   `PyQt5.QtCore.pyqtSignal`_, `PyQt6.QtCore.pyqtSignal`_,
   `PySide2.QtCore.Signal`_ or `PySide6.QtCore.Signal`_, or
   an object with a ``connect`` method of equivalent semantics,
   such as an instance of :class:`multisignal`.

   *signal* is connected to using an `AutoConnection`_ when the
   returned coroutine object is awaited.  It is disconnected from
   after the signal is emitted once.

   .. _proxyAuthenticationRequired: https://doc.qt.io/qt-6/qwebsocket.html#proxyAuthenticationRequired

   .. note::

      Signals that require immediate response from the slot cannot be used
      with this function.  An example is `proxyAuthenticationRequired`_.

   .. _destroyed: https://doc.qt.io/qt-6/qobject.html#destroyed

   .. note::

      This function will wait indefinitely if the signal is never
      emitted, e.g. if the sender object is deleted before emitting
      a signal.  To handle the latter situation, keep a strong
      reference to the sender object, or listen to its destroyed_
      signal.

.. function:: asyncsignalstream(signal: BoundSignal[typing.Unpack[Ts]]) -> typing.AsyncIterator[typing.Tuple[typing.Unpack[Ts]]]

   Return an :external:term:`asynchronous iterator` that produces the emitted arguments from *signal* as a :class:`tuple`.

   *signal* is connected to via an AutoConnection_ before the function
   returns.  It is disconnected from when the returned iterator object
   is deleted.  Emitted arguments in the interim are stored in an
   internal buffer that grows without bound.  It is advised to consume
   the iterator timely to avoid exhausting memory.

   Example:

   .. code-block:: python

      timer = QtCore.QTimer()
      timer.setInterval(1000)
      timer.start()

      what = 'tick'
      async for _ in qtinter.asyncsignalstream(timer.timeout):
          print(what)
          what = 'tock' if what == 'tick' else 'tick'

.. function:: asyncslot(fn: typing.Callable[[typing.Unpack[Ts]], typing.Coroutine[T]], *, task_runner: Callable[[typing.Coroutine[T]], asyncio.Task[T]] = qtinter.run_task) -> typing.Callable[[typing.Unpack[Ts]], asyncio.Task[T]]

   Return a callable object wrapping coroutine function *fn* so that
   it can be connected to a Qt signal.

   When the returned wrapper is called, *fn* is called with the same
   arguments to produce a coroutine object.  The coroutine object is
   then passed to *task_runner* to create an :class:`asyncio.Task`
   object that handles its execution.  The task object is returned
   by the wrapper.

   The default *task_runner*, :class:`run_task`, eagerly executes the
   task until the first ``yield``, ``return`` or ``raise`` (whichever
   comes first) before returning the task object.  The remainder of
   the coroutine is scheduled for later execution.

   .. note::

      :func:`asyncslot` keeps a strong reference to any task object
      it creates until the task completes.

   .. note::

      If *fn* is a (bound) method object, the returned wrapper will also
      be a method object whose lifetime is equal to that of *fn*, except
      that a strong reference to the returned wrapper keeps *fn* alive.

.. function:: modal(fn: typing.Callable[[typing.Unpack[Ts]], T]) -> \
              typing.Callable[[typing.Unpack[Ts]], typing.Coroutine[T]]

   Return a coroutine function that wraps a regular function *fn*.
   The coroutine function takes the same arguments as *fn*.

   When the returned coroutine function is called and awaited, *fn*
   is scheduled to be called *as interleaved code* immediately after
   the caller is suspended.  The result (exception) of *fn* is
   returned (raised) by the coroutine.

   .. note::

      This function is similar to :meth:`asyncio.loop.run_in_executor`
      except that *fn* is executed in the same thread as interleaved
      code.

   This function is designed to be called from a coroutine to schedule
   an *fn* that creates a nested Qt event loop.  In this case, the
   logical asyncio event loop is allowed to continue running without
   nesting.  For example:

   .. code-block:: python

      await qtinter.modal(QtWidgets.QMessageBox.warning)(self, "Title", "Message")

.. class:: multisignal(signal_map: typing.Mapping[BoundSignal, typing.Any])

   Collect multiple bound signals and re-emit their arguments along with
   their mapped value.

   A :class:`multisignal` object defines the following instance method:

   .. method:: connect(slot: typing.Callable[[typing.Any, typing.Tuple], typing.Any]) -> None

      Connect *slot* to each signal in (the keys of) *signal_map*,
      such that if signal *s* is mapped to *v* in *signal_map* and
      is emitted with arguments ``*args``, *slot* is called with
      ``v`` and ``args`` as arguments from the thread that called
      :meth:`connect`.  Its return value is ignored.

      The sender objects of signals in *signal_map* must be alive
      when :meth:`connect` is called, or the process will crash
      with SIGSEGV.

   :class:`multisignal` objects do not have a *disconnect* method.
   The connections are automatically disconnected when the sender
   (of a signal) or the receiver (of *slot*) is deleted.

   :class:`multisignal` may be used with :func:`asyncsignal`
   to listen to multiple signals.

   Example:

   .. code-block:: python

      fast_timer = QtCore.QTimer()
      slow_timer = QtCore.QTimer()
      # ...
      ms = qtinter.multisignal({
          fast_timer.timeout: 'fast',
          slow_timer.timeout: 'slow',
      })
      ms.connect(print)

      # Output:
      # fast ()
      # slow ()

.. function:: run_task(coro: typing.Coroutine[T], *, \
                       allow_task_nesting: bool = True, \
                       name: typing.Optional[str] = None, \
                       context: typing.Optional[contextvars.Context] = None \
              ) -> asyncio.Task[T]

   Create an :external:class:`asyncio.Task` wrapping the coroutine
   *coro* and execute it immediately until the first ``yield``,
   ``return`` or ``raise``, whichever comes first.  The remainder
   of the coroutine is scheduled for later execution.  Return the
   :external:class:`asyncio.Task` object.

   If *allow_task_nesting* is ``True`` (the default), this method
   is allowed to be called from a running task --- the calling task
   is 'suspended' before executing the first step of *coro* and
   'resumed' after that step completes.  If *allow_task_nesting*
   is ``False``, this method can only be called from a callback.

   An asyncio event loop must be running when this function is called.

   *Since Python 3.8*: Added the *name* parameter.

   *Since Python 3.11*: Added the *context* parameter.


Loop factory
------------

.. function:: new_event_loop() -> asyncio.AbstractEventLoop

   Return a new instance of an asyncio-compatible event loop object that
   runs on top of a Qt event loop.

   Use this function instead of :func:`using_qt_from_asyncio`
   if your code uses different types of event loops from multiple threads.
   For example, starting from Python 3.11, if your code uses
   :class:`asyncio.Runner` as its entry point, pass this function as the
   *loop_factory* parameter when constructing :class:`asyncio.Runner`.


Low-level classes
-----------------

You normally do not need to use these low-level API directly.


Event loop interface
~~~~~~~~~~~~~~~~~~~~

All `event loop objects`_ below are derived from the abstract base class
:class:`QiBaseEventLoop`.

.. class:: QiBaseEventLoop

   Counterpart to the (undocumented) :class:`asyncio.BaseEventLoop` class,
   implemented on top of a Qt event loop.

   In addition to asyncio's :external:ref:`asyncio-event-loop-methods`,
   this class defines the following methods for Qt interop:

   .. method:: exec_modal(fn: typing.Callable[[], typing.Any]) -> None

      Schedule *fn* to be called as interleaved code (i.e. not as a
      callback) immediately after the current callback completes.
      The return value of *fn* is ignored.

      This method must be called from a coroutine or callback.  There
      can be at most one pending *fn* at any time.

      If the current callback raises :exc:`KeyboardInterrupt` or
      :exc:`SystemExit`, *fn* will be called the next time the loop
      is run.

   .. method:: set_mode(mode: QiLoopMode) -> None:

      Set loop operating mode to *mode*.

      This method can only be called when the loop is not closed and
      not running, and no stop is pending.

      A newly created loop object is in :data:`QiLoopMode.OWNER` mode.

   .. method:: start() -> None:

      Start the loop (i.e. put it into *running* state) and return without
      waiting for it to stop.

      This method can only be called in guest mode and when the loop
      is not already running.

.. class:: QiLoopMode

   An :external:class:`enum.Enum` that defines the possible operating
   modes of a :class:`QiBaseEventLoop`.  Its members are:

   .. data:: OWNER

      Appropriate for use with asyncio-driven code.

   .. data:: GUEST

      Appropriate for use with Qt-driven code.

   .. data:: NATIVE

      Appropriate for running clean-up code.

   For details on the semantics of these modes, see :ref:`loop-modes`.


Event loop objects
~~~~~~~~~~~~~~~~~~

.. class:: QiDefaultEventLoop

   *In Python 3.7*: alias to :class:`QiSelectorEventLoop`.

   *Since Python 3.8*: alias to :class:`QiSelectorEventLoop`
   on Unix and :class:`QiProactorEventLoop` on Windows.

.. class:: QiProactorEventLoop(proactor=None)

   Counterpart to :class:`asyncio.ProactorEventLoop`, implemented on top of
   a Qt event loop.

   *Availability*: Windows.

.. class:: QiSelectorEventLoop(selector=None)

   Counterpart to :class:`asyncio.SelectorEventLoop`, implemented on top of
   a Qt event loop.


Event loop policy objects
~~~~~~~~~~~~~~~~~~~~~~~~~

.. class:: QiDefaultEventLoopPolicy

   *In Python 3.7*: alias to :class:`QiSelectorEventLoopPolicy`.

   *Since Python 3.8*: alias to :class:`QiSelectorEventLoopPolicy`
   on Unix and :class:`QiProactorEventLoopPolicy` on Windows.

.. class:: QiProactorEventLoopPolicy

   Event loop policy that creates :class:`QiProactorEventLoop`.

   *Availability*: Windows.

.. class:: QiSelectorEventLoopPolicy

   Event loop policy that creates :class:`QiSelectorEventLoop`.


Private API
-----------

The following classes and functions are used internally to support
:mod:`qtinter`'s implementation.  They are documented here solely
for developing :mod:`qtinter`, and are subject to change at any time.

.. class:: SemiWeakRef(o, ref=weakref.ref)

   Return an object that is deleted when *o* is deleted, except that
   a strong reference to the returned object in user code keeps *o*
   alive.

   *ref* should be a weak reference class suitable for *o*: If *o* is
   a method object, *ref* should be set to :class:`weakref.WeakMethod`;
   otherwise, *ref* should be set to :class:`weakref.ref`.

   .. method:: referent()

      Return *o* if it is still live, or ``None``.

.. function:: copy_signal_arguments(args: typing.Tuple[typing.Unpack[Ts]]) -> typing.Tuple[typing.Unpack[Ts]]

   Return a copy of signal arguments *args* where necessary.

   In PyQt5/6, signal arguments passed to a slot may be temporary objects
   whose lifetime is only valid during the slot's execution.  In order to
   use the signal arguments after the slot returns, one must call this
   function to make a copy of them, or the program may crash with SIGSEGV
   when the signal arguments are accessed later.

   PySide2/6 already passes a copy of the signal arguments to slots,
   whose lifetime is controlled by the usual Python mechanisms.  This
   function returns *args* as is in this case.

.. function:: get_positional_parameter_count(fn: typing.Callable) -> int

   Return the number of positional parameters of *fn*, or ``-1``
   if *fn* takes variadic positional parameters (``*args``).

   Raises :class:`TypeError` if *fn* takes any keyword-only parameter
   without a default.

.. function:: transform_slot(slot: typing.Callable[[typing.Unpack[Ts]], T], transform: typing.Callable[[typing.Callable[[typing.Unpack[Ts]], T], typing.Tuple[typing.Unpack[Rs]], typing.Unpack[Es]], R], *extras: typing.Unpack[Es]) -> typing.Callable[[typing.Unpack[Rs]], R]

   Return a callable *wrapper* that takes variadic arguments ``*args``,
   such that ``wrapper(*arg)`` returns ``transform(slot, args, *extra)``.

   If *slot* is a bound method object, *wrapper* will also be a bound
   method object with the same lifetime as *slot*, except that a strong
   reference to *wrapper* keeps *slot* alive.

   If *slot* is not a bound method object, *wrapper* will be a function
   object that holds a strong reference to *slot*.

