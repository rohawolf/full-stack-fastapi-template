# Infrastructure

> In this layer we place the input and output adapters, which implement the interfaces defined for the repositories or business events.

For example:
- Repository that stores the data in a database.
- Events that communicate with some queuing engine.
- Handlers that serve as the entry point and that call the application services.
- In this layer we can implement any 3rd party library.