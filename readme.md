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

<img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/Kin-TXT-architecture.jpg?raw=true" width="1000" alt="Architecture Diagram"> 

## Custom Reports-Builder for Advanced Text Classification
Kin-TXT allows users to easily adapt the platform for their own needs. You can fork Kin-TXT and create a new "reports-builder" to handle specific text classification tasks. This is ideal for projects that need unique logic for analyzing and classifying text data. Whether it's for a specialized project or advanced research, Kin-TXT makes it simple to incorporate your own classification rules and logic.  


# Usage

### View Your Reports
Easily access and review your generated reports. Our streamlined interface allows for quick navigation and in-depth analysis of your data.

<p align="center">
  <img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image1.png" width="700" alt="View Reports">
</p>

### Upload Your Own Models or Use Built-In
Kin-TXT supports both custom models and a selection of built-in models, giving you the flexibility to approach data analysis in the way that best suits your project's needs.

<p align="center">
  <img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image4.png" width="500" alt="Upload Models">
  <img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image3.png" width="500" alt="List models">
</p>

### Create Visualization Charts That Suit Your Needs
Transform your data into compelling visual stories with our customizable charting tools. Whether you're presenting results or exploring data, our visualizations help you convey information clearly and effectively.

<p align="center">
  <img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image7.png" width="1000" alt="Create Visualization Charts">
</p>

## Reports visualization
Kin-TXT enhances your data analysis experience with powerful visualization features, enabling you to gain deeper insights into your data. Here are two key visualization capabilities:

### Statistical Reports with Specified Charts
Our statistical reports feature allows you to visualize your data through a variety of specified charts, including bar graphs, line charts, pie charts, and more. This flexibility ensures that you can present your data in the format that best represents the underlying trends and patterns, making it easier to understand and communicate your findings.

<p align="center">
  <img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image6.png" width="900" alt="Statistical report">
</p>

### Word Cloud Report
The word cloud report feature provides a visual representation of text data, highlighting the most frequent terms in your dataset in a dynamic and engaging format. This is particularly useful for analyzing textual data like customer feedback, social media posts, or any large corpus of text, helping you quickly identify prominent themes and keywords.  

Word cloud also allows you to filter out your custom words. See the data only from specific data source and filter by predicted category.

<p align="center">
  <img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image9.png" width="900" alt="Word Cloud Report">
</p>

### Compare reports  
You can also compare two or your reports in app

<p align="center">
  <img src="https://github.com/kinfi4/Kin-Txt/blob/master/docs/pictures/image8.png" width="1000" alt="Word Cloud Report">
</p>


-----
@kinfi4
