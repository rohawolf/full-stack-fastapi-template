# Structure

```bash
├── app
│   ├── application 
│   │   ├── validators # Validation logic for input data
│   │   └── services # Implement the use cases
│   ├── domain
│   │   ├── entities # Entities with business logic
│   │   ├── events # Interface that defines how an event behaves
│   │   ├── repositories # Interface that defines how a data repository behaves
│   │   ├── use cases # Interface that defines the use cases of the application
│   │   └── exceptions # Domain exceptions
│   ├── infrastructure
│   │   ├── events # Implements the domain event interface
│   │   ├── handlers # Application entry point
│   │   ├── repositories # Implements the domain repository interface
│   │   ├── schemas # Data structures used as input and output
│   │   └── container # Dependency injector
└───└── test
```

**references**

- https://codesandbox.io/p/github/Anderson-Pozo/fastapi-hexagonal/main