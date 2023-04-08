## Introduction

**Notery** is an automation utility for converting Google Keep notes into zettelkasten notes. 

<br>

## Motivation
Two guiding principles serve as the motivation for development of **Notery**. First, eliminate or dramatically reduce the amount of physical paper used in my research workflows. Doing so is harder than it might seem given how unforgiving a digital workflow is compared to using physical paper. Second, the entry point (i.e., Google Keep) must be portable and available 24x7x365 with very low use friction. As much as I enjoy using Markdown with Obsidian for example, I'm not running that toolchain on my mobile device. 

<br>

## Worfklow

Notery is simple: it finds notes in Google Keep based on predefined labels (read: tags), writes them to local disk in a standardized zettelkasten format, and then archives those notes in Keep. The `find` ignores Keep notes that have been archived.

<br>

# Installation
Installation is simple. The steps are:

1. Clone this repo: `git clone git@github.com:jasonmpittman/notery.git`

2. I think running **Notery** from a virtual environment is a good idea. While there are no unsafe dependencies or risky functions, the organization and containment of `venv` is handy. If you want to do the same:

    `cd notery`  
    `pip install -r requirements.txt`  

    If you don't care about `venv`, you can skip this step.

3. Define account credentials in credentials.json  
Create a json file and add the following. Note: I would use an app password and not your Google account password. You can set this up using the [Google procedure](https://myaccount.google.com/apppasswords)

You have to activate the 2 factor authentication in your Google account and then you have to create an application password for gkeepapi. That's the password you use instead of your Google account password.

Then you have to use the application password instead your usual password in keep.login function (the username is the same).).

    ```
    {
        "UserName": "youremail@gmail.com",
        "Password": "password"
    }
    ```


4. Edit default list of labels (tags) in tags.json  
Edit or create another json file and add the following with the Keep labels you want to target:

    ```
    {
        "Tags": ["reference,fleeting,permanent"]
    }
    ```

5. Edit the target directory for writing zettels in config.ini  
Edit the `config.ini` with the full path to where you want **Notery** to write the converted zettels.
  
<br>

## Running Notery
Notery is easy to use. From a shell, run `python3 notery.py -w` and you are done. You can also list the Keep notes without writing them to local disk using `pyhton3 notery.py -l`.

<br>

## To Do

I don't think Notery is complete as a fully functional tool. As a beta release, it works as intended however I know I want:

1. The ability to search for Google Keep notes by label and list matches by title. 

2. The ability to specify labels (read: tags) at runtime to override the `tags.json`.

3. More interactivity during the conversion process. Perhaps a confirmation of the notes to be converted and optional progress output (i.e., normal and verbose modes).