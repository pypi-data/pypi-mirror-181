<h1 align="center">DS Template 👨‍💻</h1>
<p>
  <a href="#" target="_blank">
  <img alt="Version" src="https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000" />
  </a>
  <a href="#" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-pdoc-orange.svg" />
  </a>
  <a href="LICENSE" target="_blank">
    <img alt="License: Adel Rayane Amrouche" src="https://img.shields.io/badge/License-Adel Rayane Amrouche-yellow.svg" />
  </a>
</p>

> Template to Kickstart Data Science projects that follows Sklearn standards and brings usefull tools to handle data and models quickly and easily

## Install

```sh
pip install poetry
poetry install
```

## Run tests

```sh
pytest src/
pylint src/
mypy src/
```

## Documentation

```sh
pdoc src/
```

### Usage

The DS Template has 3 main components:
- A **DataManager** component
- A **Controller** component
- A **Model** component

The latter depends on the projects type and can be let empty if no model is needed.

That lets us with both the **controller** and the **data manager**. On the one hand, the **controller** is supposed to be the center of the project and interact with all the components to get the output asked by the user. On the other hand, the **data manager** is working around a json metadata file. This metafile follows a specific schema for both input sources and output sources.

#### Input Sources
> Sources can take 2 inputs regardless of the type of source and regardless if it is an intput or an output source:
> - A **type** that can be either **csv**, **excel** or **sql**.
> - A list of **args** that will be executed by pandas to get access to the source and prepare correctly the dataset.
>
> Three kind of **input** sources are handled :
> - The **local** files that only take a **path** to the source file
> - The **sharepoint** files that take:
>   - The **sharepoint** address and the **sites** where the source is
>   - The **folder** where the file source is
>   - The **file** source name
> - The **Sql** sources that take:
>   - An **username** and a **password** environment variables names
>   - An **address** of the database and **dialect** of the sql type of database
>   - A **query** which is not mandatory since sql sources can be handled as a database instead of a simple dataset. You will be then able to query this database like you would do using *sqlalchemy*

*Samples are available in the file **data/metadata.json***

> Two kind of **output** sourcess are handled :
> - The **local** files that only take a **path** to the source file
> - The **Sql** sources that take:
>   - An **username** and a **password** environment variables names
>   - An **address** of the database and **dialect** of the sql type of database
>   - A **table_name** where the dataset will be added
>   - You also might need to include the **schema** and the parameter **if_exists** (either "replace" or append" regarding the way you want to update the table) in the list of **args** 

## Author

👤 **Rayane Amrouche**

* Github: [@AARayane](https://github.com/AARayane)
