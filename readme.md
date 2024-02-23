<img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image-logo.png" width="100" alt="Kin-TXT Logo"> 

# Kin-TXT

Kin-TXT is an open-source platform designed to simplify the way users interact with NLP text classification models and data visualization. It enables users to upload machine learning models created with Keras or sklearn and provides tools for visualizing data in various formats. The platform is particularly useful for those looking to analyze and present data gathered from specified Telegram channels, with plans to expand to more data sources in the future.

The platform empowers users to define detailed preprocessing steps for their machine-learning models, ensuring that data is optimally prepared before analysis. This feature allows for the customization of data cleaning or normalization.

Current solution might be suitable for a range of applications, including:    

   * Education: A practical tool for learning about machine learning and data analysis.
   * Research: Useful for data visualization and analysis in academic and scientific research.
   * Development: Helps developers test and refine machine learning models.
   * Personal Projects: Ideal for anyone interested in exploring machine learning and data visualization.

## Architecture

Kin-TXT is structured around six key components, each designed to offer a streamlined workflow for machine learning model management, data visualization, and report generation:

* **kin-api-gateway**: Acts as the primary router for all incoming requests, directing them to the appropriate services within the Kin-TXT ecosystem. It focuses on efficient request handling and routing without incorporating additional security features.

* **kin-builtin-models-reports-builder**: Functions as a dedicated service for generating reports using predefined models. It operates as a RabbitMQ consumer, processing commands and executing report building tasks in a Celery environment. This component is essential for users who rely on built-in models for their data analysis.

* **kin-frontend**: Provides a Single Page Application (SPA) interface, enabling users to interact with Kin-TXT's features in a seamless and intuitive manner. The frontend is the visual and interactive layer through which users manage models, initiate report building, and view visualizations.

* **kin-generic-reports-builder**: Serves as a repository and execution environment for user-uploaded model binaries. It listens for report building commands via RabbitMQ and performs the report generation tasks in Celery. This component allows users to incorporate their custom logic and models into the Kin-TXT platform.

* **kin-model-types**: Stores metadata about both user-uploaded and built-in models, along with visualization templates. This service ensures that the platform can effectively manage and utilize various model types and visualization approaches, enhancing the flexibility and customization capabilities of Kin-TXT.

* **kin-statistics**: Responsible for storing the generated reports. This component not only archives the outcomes of data analysis but also serves as a resource for reviewing and accessing past insights.

<img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/Kin-TXT-architecture.jpg?raw=true" width="1000" alt="Kin-TXT Logo"> 

## Custom Reports-Builder for Advanced Text Classification
Kin-TXT allows users to easily adapt the platform for their own needs. You can fork Kin-TXT and create a new "reports-builder" to handle specific text classification tasks. This is ideal for projects that need unique logic for analyzing and classifying text data. Whether it's for a specialized project or advanced research, Kin-TXT makes it simple to incorporate your own classification rules and logic.  


