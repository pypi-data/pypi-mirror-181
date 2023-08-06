"""Hello! This is basically me."""


class CtrlManiac:
    """CtrlManiac because i overuse the ctrl key."""

    def __init__(self):
        """My specifications."""
        self.name = "Davide"
        self.surname = "Di Criscito"
        self.nickname = "Dave"
        self.pronouns = (
            "He",
            "Him",
        )

        self.languages_spoken = ["it_IT", "en_US", "en_GB"]

        self.description = (
            "I'm currently an Artisan, soon-to-be a full-stack web developer!"
        )

        self.websites = [
            "https://ctrlmaniac.me",
            "https://www.linkedin.com/in/dcdavide/",
        ]

        self.hobbies = [
            "coding",
            "hiking",
            "photography",
            "watching movies & TV series",
            "listening to music",
            "reading books and manga",
            "going out with my friends and have fun",
        ]

        self.coding_languages = [
            "Python",  # I simply love it
            "JavaScript",
            "Typescript",
            "Java",
            "Golang",
        ]

        self.favourite_tools = [
            "poetry",  # makes it simpler to manage a python project
            "black",  # chooses a coding style for me and makes my code pretty
            "isort",  # sorts python imports so that everything is really clear
            "flake8",  # tells me whether I've made a mistake
            "pydocstyle",  # helps me write better documentation
            "yarn",  # I love it for the workspace feature
            "lerna",  # I use it to manage my monorepos
            "prettier",  # chooses a coding style for me and makes my code pretty
        ]

        self.IDEs = [
            "VScode",  # because it's awesome!
        ]

    def greet(self) -> None:
        """Say hi."""
        print(
            f"Hi! I'm {self.name} {self.surname}, but you can call me {self.nickname}."
        )
        print(self.description)
        print(f"You can know more about me by visiting my website: {self.websites[0]}")
