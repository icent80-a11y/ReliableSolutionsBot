# Overview

This project is a Telegram bot for "Надежные-решения.рф" (Reliable Solutions), a Russian fulfillment services company. The bot provides an interactive platform for potential clients to calculate fulfillment costs for major Russian marketplaces (Wildberries, Ozon, Yandex Market), submit service applications, and learn about company services. The bot features a cost calculator that estimates pricing based on marketplace choice, order volume, and selected services, along with conversation flows for lead generation and customer service.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Bot Framework Architecture
The application uses the python-telegram-bot library built on the PTB (Python Telegram Bot) framework. The architecture follows a modular handler-based pattern with ConversationHandler for managing multi-step user interactions. State management is implemented through predefined conversation states for calculator flows and application submission processes.

## Conversation Flow Design
The system implements two main conversation flows: a cost calculator flow (marketplace selection → order count input → service selection → result display) and an application submission flow (name input → contact collection → description gathering). Each flow uses state-based navigation with fallback handlers to ensure robust user experience.

## Data Management Strategy
The application uses in-memory configuration-based data storage for tariffs and service pricing. All marketplace tariffs, service rates, and pricing logic are defined in static configuration files rather than a database. This approach prioritizes simplicity and eliminates external dependencies for a relatively static dataset.

## Message and UI Architecture
The bot implements a structured messaging system with predefined message templates stored in a centralized messages module. User interface elements use inline keyboard markup for navigation and selection, providing a native Telegram experience. The formatting system includes specialized functions for presenting calculation results in a readable format.

## Service Calculation Engine
The core business logic centers around a FulfillmentCalculator class that processes marketplace-specific pricing, applies volume discounts, and calculates service costs. The calculator supports multiple service types (storage, packaging, shipping, returns, labeling, quality control, photography) with different rate structures and applies marketplace-specific commission rates.

## Configuration Management
The system uses environment variable configuration for sensitive data (bot tokens) while maintaining business logic configuration in Python modules. This hybrid approach provides security for credentials while keeping business rules easily maintainable and version-controlled.

# External Dependencies

## Telegram Bot Platform
The application integrates with Telegram's Bot API through the python-telegram-bot library. This handles all communication with Telegram servers, message processing, and user interaction management. The bot requires a valid Telegram Bot Token from BotFather for operation.

## Python Runtime Environment
The system requires Python 3.x runtime with the telegram library for bot functionality. The application uses standard Python logging for operational monitoring and debugging capabilities.

## Environment Configuration
The bot expects the TELEGRAM_BOT_TOKEN environment variable to be configured for authentication with Telegram's API. No other external services or databases are required for core functionality.

## Marketplace Integration Preparation
While not currently implemented, the configuration suggests future integration capabilities with marketplace APIs (Wildberries API, Ozon API, Yandex Market API) for real-time data synchronization and automated order processing.