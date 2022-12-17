from typing import Protocol


class WebDriver(Protocol):

    def render(self, html: str) -> str:
        """
            Receive an html page in string format and execute the javascript
            returning the new rendered html
        """
        ...