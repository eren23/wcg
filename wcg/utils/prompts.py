# used the prompt example from the repo as base, updated and improved a little bit
# https://github.com/lavague-ai/LaVague
prompt_template_selenium = '''

Your objective is to craft Selenium Python code snippets to fulfill specific actions on a web page. 
Your solutions must be encapsulated in Python code cells, considering external web resources and libraries as accessible. 
Pay close attention to the uniqueness of attribute values when targeting elements on the page. Where possible, employ a blend of text content, class names, or IDs for a more precise element targeting strategy. 
In scenarios where multiple elements share similar functions, prioritize accuracy by selecting the most relevant element. 
Utilize the contains@class syntax for targeting elements with multiple classes.

Prior to writing your code, assume the initial setup below has already been executed:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
```

---

HTML:
<body>
    <h1>Search Page Example</h1>
    <input id="searchBar" type="text" placeholder="Type here to search...">
    <button id="searchButton">Search</button>
    <script>
        document.getElementById('searchButton').onclick = function() {{
            var searchText = document.getElementById('searchBar').value;
            alert("Searching for: " + searchText);
        }};
    </script>
</body>

Query: Click on the search bar 'Type here to search...', type 'selenium', and press the 'Enter' key

Completion:
```python
# Let's proceed step by step.
# First we need to identify the component first, then we can click on it.

# Based on the HTML, the link can be uniquely identified using the ID "searchBar"
# Let's use this ID with Selenium to identify the link
search_bar = driver.find_element(By.XPATH, "//*[@id='searchBar']")

search_bar.click()

# Now we can type the asked input
search_bar.send_keys("selenium")

# Finally we can press the 'Enter' key
search_bar.send_keys(Keys.ENTER)
```

---

HTML:

<body>
    <h1>Welcome to the Mock Page</h1>
    <div id="links">
        <a href="#link1" id="link1">Link 1</a>
        <br>
        <a href="#link2" class="link">Link 2</a>
        <br>
    </div>
</body>

Query: Click on the title Link 1 and then click on the title Link 2

Completion:
```python
# Let's proceed step by step.
# First we need to identify the first component, then we can click on it. Then we can identify the second component and click on it.

# Based on the HTML, the first link the link can be uniquely identified using the ID "link1"
# Let's use this ID with Selenium to identify the link
link_to_click = driver.find_element(By.XPATH, "//*[@id='link1']")

# Then we click on the link
link_to_click.click()

# The other link can be uniquely identified using the class "link"
# Let's use this class to identify the link
link_to_click = driver.find_element(By.XPATH, "//*[@class='link']")

# Click on the element found
link_to_click.click()
```

---

HTML:
<body>
    <p id="para1">This is the first paragraph.</p>
    <p id="para2">This is the second paragraph.</p>
    <p id="para3">This is the third paragraph, which we will select and copy.</p>
    <p id="para4">This is the fourth paragraph.</p>
</body>

Query: Select the text inside the third paragraph

Completion:
```python
# Let's proceed step by step.

# To select a paragraph, we can execute a JS script to select the text using the DOM
# In the provided HTML, the third paragraph can be identified using the ID "para3"
# We need to use getElementById to select the paragraph precisely
js_script = """
    // This part depends on the specific HTML, here is the identified ID "para3"
    var para = document.getElementById('para3');
    // The rest is standard
    if (document.body.createTextRange) {{
        var range = document.body.createTextRange();
        range.moveToElementText(para);
        range.select();
    }} else if (window.getSelection) {{
        var selection = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(para);
        selection.removeAllRanges();
        selection.addRange(range);
    }}
"""

# Then we execute JavaScript
driver.execute_script(js_script)
```

---

HTML:

Query: Scroll up a bit

Completion:
```python
# Let's proceed step by step.
# We don't need to use the HTML data as this is a stateless operation.
# 200 pixels should be sufficient. Let's execute the JavaScript to scroll up.

driver.execute_script("window.scrollBy(0, 200)")
```

---

HTML:
<body>
    <form id="registrationForm">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <button type="submit">Register</button>
    </form>
</body>



Query: Fill out the registration form with the username 'new_user' and password 'securepassword123'

Completion:
```python
# Identifying the username and password input fields and the submit button
username_input = driver.find_element(By.ID, "username")
password_input = driver.find_element(By.ID, "password")
submit_button = driver.find_element(By.XPATH, "//form[@id='registrationForm']//button[@type='submit']")

# Filling out the form
username_input.send_keys("new_user")
password_input.send_keys("securepassword123")

# Submitting the form
submit_button.click()
```

---
HTML:
<body>
    <label for="favoriteColor">Choose your favorite color:</label>
    <select id="favoriteColor" name="favoriteColor">
        <option value="red">Red</option>
        <option value="blue">Blue</option>
        <option value="green">Green</option>
        <option value="yellow">Yellow</option>
    </select>
    <button id="submitColor">Submit</button>
</body>

Query: Select the option 'Blue' from the dropdown menu and click the submit button

Completion:
```python
from selenium.webdriver.support.ui import Select

# Locating the dropdown menu
favorite_color_dropdown = Select(driver.find_element(By.ID, "favoriteColor"))

# Selecting an option from the dropdown. Here, "Blue" is selected by visible text
favorite_color_dropdown.select_by_visible_text("Blue")

# Finding and clicking the submit button
submit_button = driver.find_element(By.ID, "submitColor")
submit_button.click()
```

---

HTML:
{context_str}
Query: {query_str}
Completion:
'''

prompt_template_js = """
Your mission is to develop JavaScript code snippets capable of performing specified tasks on web pages. Ensure your responses are structured strictly as JavaScript code. Consideration for external web resources and libraries is permitted and encouraged to enhance functionality or streamline solutions.

When engaging with DOM elements, avoid making assumptions about the uniqueness of attribute values. Instead, refine your selection criteria by leveraging a mix of text content, class names, or IDs. This approach aids in accurately pinpointing the desired element amidst potential duplicates. In scenarios where numerous elements share similar functionalities, execute due diligence to identify and interact with the element most closely aligned with the task's requirements.

Emphasize the utilization of querySelector and querySelectorAll for DOM manipulation. These methods provide a robust framework for element selection, accommodating complex selectors that can combine attribute values, class names, and pseudo-classes, among other criteria.

You can assume the following code has been executed:
```javascript
document.addEventListener('DOMContentLoaded', (event) => {{
    console.log('DOM fully loaded and parsed');
}});
```
---

HTML:

<body>
    <h1>Search Page Example</h1>
    <input id="searchBar" type="text" placeholder="Type here to search...">
    <button id="searchButton">Search</button>
    <script>
        document.getElementById('searchButton').onclick = function() {{
            var searchText = document.getElementById('searchBar').value;
            alert("Searching for: " + searchText);
        }};
    </script>
</body>

Query: Click on the search bar 'Type here to search...', type 'selenium', and press the 'Enter' key

Completion:
```javascript
// First, let's select the search bar using its ID.
const searchBar = document.querySelector('#searchBar');

// Simulate a click action on the search bar.
searchBar.click();

// Now, we can simulate typing 'selenium' into the search bar.
searchBar.value = 'selenium';

// To simulate pressing the 'Enter' key, we create a new event for the 'Enter' key and dispatch it.
const enterKeyEvent = new KeyboardEvent('keypress', {{'key': 'Enter'}});
searchBar.dispatchEvent(enterKeyEvent);
```
---

HTML:


<body>
    <h1>Welcome to the Mock Page</h1>
    <div id="links">
        <a href="#link1" id="link1">Link 1</a>
        <br>
        <a href="#link2" class="link">Link 2</a>
        <br>
    </div>
</body>

Query: Click on the title Link 1 and then click on the title Link 2

Completion:
```javascript
// To click on Link 1, we select it by its ID and simulate a click.
document.querySelector('#link1').click();

// Next, to click on Link 2, we select it by its class name and simulate a click.
document.querySelector('.link').click();
```
---

HTML:

<body>
    <p id="para1">This is the first paragraph.</p>
    <p id="para2">This is the second paragraph.</p>
    <p id="para3">This is the third paragraph, which we will select and copy.</p>
    <p id="para4">This is the fourth paragraph.</p>
</body>

Query: Select the text inside the third paragraph

Completion:

```javascript
// To select the text of the third paragraph, we use its ID.
const para3 = document.querySelector('#para3');
const range = document.createRange();
const selection = window.getSelection();

// Clear any previous selections
selection.removeAllRanges();

// Select the paragraph's text
range.selectNodeContents(para3);
selection.addRange(range);
```

---

HTML:

<body>
    <form id="registrationForm">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <button type="submit">Register</button>
    </form>
</body>

Query: Fill out the registration form with the username 'new_user' and password 'securepassword123'

```javascript
// Function to fill out and submit the registration form
function submitRegistrationForm(username, password) {{
    // Select the username and password input fields
    const usernameInput = document.querySelector('#username');
    const passwordInput = document.querySelector('#password');

    // Check if both input fields are found
    if (!usernameInput || !passwordInput) {{
        console.error('Input fields not found');
        return;
    }}

    // Set the input values
    usernameInput.value = username;
    passwordInput.value = password;

    // Find and submit the form
    const form = document.querySelector('#registrationForm');
    if (form) {{
        form.submit();
    }} else {{
        console.error('Registration form not found');
    }}
}}

// Example usage
submitRegistrationForm('new_user', 'securepassword123');
```

---

HTML:

<body>
    <label for="favoriteColor">Choose your favorite color:</label>
    <select id="favoriteColor" name="favoriteColor">
        <option value="red">Red</option>
        <option value="blue">Blue</option>
        <option value="green">Green</option>
        <option value="yellow">Yellow</option>
    </select>
    <button id="submitColor">Submit</button>
</body>

Query:  Select the option 'Blue' from the dropdown menu and click the submit button

```javascript
// Function to select a favorite color and submit the survey form
function submitFavoriteColor(color) {{
    // Select the dropdown element by its ID
    var colorDropdown = document.querySelector('#favoriteColor');
    // Select the submit button by its ID
    var submitButton = document.querySelector('#submitColor');

    // Set the value of the dropdown to the desired color
    colorDropdown.value = color;

    // Check if the selected color option exists
    if (colorDropdown.value !== color) {{
        console.error('Color option not found:', color);
        return;
    }}

    // Submit the survey by clicking the submit button
    // This action could vary depending on how the survey is processed
    submitButton.click();
}}
// Example usage
submitFavoriteColor('blue');
```

---

HTML:
{context_str}
Query: {query_str}
Completion:
"""

selenium_few_shot = [
    {
        "query": """Click on the search bar 'Type here to search...', type 'selenium', and press the 'Enter' key""",
        "example": """
        HTML:
        <body>
            <h1>Search Page Example</h1>
            <input id="searchBar" type="text" placeholder="Type here to search...">
            <button id="searchButton">Search</button>
            <script>
                document.getElementById('searchButton').onclick = function() {{
                    var searchText = document.getElementById('searchBar').value;
                    alert("Searching for: " + searchText);
                }};
            </script>
        </body>

        Query: Click on the search bar 'Type here to search...', type 'selenium', and press the 'Enter' key

        Completion:
        ```python
        # Let's proceed step by step.
        # First we need to identify the component first, then we can click on it.

        # Based on the HTML, the link can be uniquely identified using the ID "searchBar"
        # Let's use this ID with Selenium to identify the link
        search_bar = driver.find_element(By.XPATH, "//*[@id='searchBar']")

        search_bar.click()

        # Now we can type the asked input
        search_bar.send_keys("selenium")

        # Finally we can press the 'Enter' key
        search_bar.send_keys(Keys.ENTER)
        ```
    """,
    },
    {
        "query": """Click on the title Link 1 and then click on the title Link 2""",
        "example": """
        HTML:

        <body>
            <h1>Welcome to the Mock Page</h1>
            <div id="links">
                <a href="#link1" id="link1">Link 1</a>
                <br>
                <a href="#link2" class="link">Link 2</a>
                <br>
            </div>
        </body>

        Query: Click on the title Link 1 and then click on the title Link 2

        Completion:
        ```python
        # Let's proceed step by step.
        # First we need to identify the first component, then we can click on it. Then we can identify the second component and click on it.

        # Based on the HTML, the first link the link can be uniquely identified using the ID "link1"
        # Let's use this ID with Selenium to identify the link
        link_to_click = driver.find_element(By.XPATH, "//*[@id='link1']")

        # Then we click on the link
        link_to_click.click()

        # The other link can be uniquely identified using the class "link"
        # Let's use this class to identify the link
        link_to_click = driver.find_element(By.XPATH, "//*[@class='link']")

        # Click on the element found
        link_to_click.click()
        ```
        """,
    },
    {
        "query": """Scroll up a bit""",
        "example": """
        HTML:

        Query: Scroll up a bit

        Completion:
        ```python
        # Let's proceed step by step.
        # We don't need to use the HTML data as this is a stateless operation.
        # 200 pixels should be sufficient. Let's execute the JavaScript to scroll up.

        driver.execute_script("window.scrollBy(0, 200)")
        ```
        """,
    },
    {
        "query": """Fill out the registration form with the username 'new_user' and password 'securepassword123'""",
        "example": """
        HTML:
        <body>
            <form id="registrationForm">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <button type="submit">Register</button>
            </form>
        </body>



        Query: Fill out the registration form with the username 'new_user' and password 'securepassword123'

        Completion:
        ```python
        # Identifying the username and password input fields and the submit button
        username_input = driver.find_element(By.ID, "username")
        password_input = driver.find_element(By.ID, "password")
        submit_button = driver.find_element(By.XPATH, "//form[@id='registrationForm']//button[@type='submit']")

        # Filling out the form
        username_input.send_keys("new_user")
        password_input.send_keys("securepassword123")

        # Submitting the form
        submit_button.click()
        ```
        """,
    },
    {
        "query": """Select the option 'Blue' from the dropdown menu and click the submit button""",
        "example": """
        HTML:
        <body>
            <label for="favoriteColor">Choose your favorite color:</label>
            <select id="favoriteColor" name="favoriteColor">
                <option value="red">Red</option>
                <option value="blue">Blue</option>
                <option value="green">Green</option>
                <option value="yellow">Yellow</option>
            </select>
            <button id="submitColor">Submit</button>
        </body>

        Query: Select the option 'Blue' from the dropdown menu and click the submit button

        Completion:
        ```python
        from selenium.webdriver.support.ui import Select

        # Locating the dropdown menu
        favorite_color_dropdown = Select(driver.find_element(By.ID, "favoriteColor"))

        # Selecting an option from the dropdown. Here, "Blue" is selected by visible text
        favorite_color_dropdown.select_by_visible_text("Blue")

        # Finding and clicking the submit button
        submit_button = driver.find_element(By.ID, "submitColor")
        submit_button.click()
        ```
        """,
    },
    {
        "query": """Select the text inside the third paragraph""",
        "example": '''
        HTML:
        <body>
            <p id="para1">This is the first paragraph.</p>
            <p id="para2">This is the second paragraph.</p>
            <p id="para3">This is the third paragraph, which we will select and copy.</p>
            <p id="para4">This is the fourth paragraph.</p>
        </body>

        Query: Select the text inside the third paragraph

        Completion:
        ```python
        # Let's proceed step by step.

        # To select a paragraph, we can execute a JS script to select the text using the DOM
        # In the provided HTML, the third paragraph can be identified using the ID "para3"
        # We need to use getElementById to select the paragraph precisely
        js_script = """
            // This part depends on the specific HTML, here is the identified ID "para3"
            var para = document.getElementById('para3');
            // The rest is standard
            if (document.body.createTextRange) {{
                var range = document.body.createTextRange();
                range.moveToElementText(para);
                range.select();
            }} else if (window.getSelection) {{
                var selection = window.getSelection();
                var range = document.createRange();
                range.selectNodeContents(para);
                selection.removeAllRanges();
                selection.addRange(range);
            }}
        """

        # Then we execute JavaScript
        driver.execute_script(js_script)
        ```
        ''',
    },
    {
        "query": """Select the option 'Motorcycle' from the dropdown menu and click the submit button.""",
        "example": """
        HTML:
        <body>
            <label for="vehicleChoice">Select your vehicle type:</label>
            <select id="vehicleChoice" name="vehicleChoice">
                <option value="car">Car</option>
                <option value="truck">Truck</option>
                <option value="motorcycle">Motorcycle</option>
                <option value="bicycle">Bicycle</option>
            </select>
            <button id="submitVehicle">Submit Vehicle Type</button>
        </body>
        
        Query: Select the option 'Motorcycle' from the dropdown menu and click the submit button.
        
        Completion:
        ```python

        # Find the dropdown element by its ID and create a Select object
        vehicle_select = Select(driver.find_element(By.ID, "vehicleChoice"))

        # Select the option by visible text
        vehicle_select.select_by_visible_text("Motorcycle")

        # Find the submit button by its ID and click it
        submit_button = driver.find_element(By.ID, "submitVehicle")
        submit_button.click()
        ```
        """,
    },
    {
        "query": """Select the option 'Cherry' from the dropdown menu and click the submit button.""",
        "example": """
        HTML:
        <body>
            <label for="fruitChoice">Choose a fruit:</label>
            <select id="fruitChoice" name="fruitChoice">
                <option value="apple">Apple</option>
                <option value="banana">Banana</option>
                <option value="cherry">Cherry</option>
                <option value="date">Date</option>
            </select>
            <button id="submitFruit">Submit Choice</button>
        </body>
        
        Query: Select the option 'Cherry' from the dropdown menu and click the submit button.
        
        Completion:
        ```python
        # Find the dropdown for fruits by its ID and create a Select object
        fruit_select = Select(driver.find_element(By.ID, "fruitChoice"))

        # Select the fruit by visible text
        fruit_select.select_by_visible_text("Cherry")

        # Find the submit button by its ID and click it
        submit_button = driver.find_element(By.ID, "submitFruit")
        submit_button.click()
        ```
        """,
    },
    {
        "query": "Select the radio button for a rating of '4' and submit the form.",
        "example": """
        HTML:
        <body>
            <label for="rating">Rate our service:</label>
            <form id="serviceRating">
                <input type="radio" id="rate1" name="rating" value="1"><label for="rate1">1</label>
                <input type="radio" id="rate2" name="rating" value="2"><label for="rate2">2</label>
                <input type="radio" id="rate3" name="rating" value="3"><label for="rate3">3</label>
                <input type="radio" id="rate4" name="rating" value="4"><label for="rate4">4</label>
                <input type="radio" id="rate5" name="rating" value="5"><label for="rate5">5</label>
                <button type="submit">Submit Rating</button>
            </form>
        </body>
        
        Query: Select the radio button for a rating of '4' and submit the form.

        ```python
        # Select the radio button for the rating 4
        radio_button = driver.find_element(By.ID, "rate4")
        radio_button.click()

        # Find and click the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        ```
        """,
    },
    {
        "query": "Enter the email address 'user@example.com' into the email input field and click the subscribe button.",
        "example": """
        <body>
            <h2>Subscribe to our Newsletter</h2>
            <form id="newsletterForm">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" placeholder="Enter your email">
                <button type="submit">Subscribe</button>
            </form>
        </body>
        
        Query: Enter the email address user@example.com into the email input field and click the subscribe button.
        
        Completion:
        ```python
        # Enter an email into the email input field
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys("user@example.com")

        # Find and click the subscribe button
        subscribe_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        subscribe_button.click()
        ```
        """,
    },
]

js_few_shot = [
    {
        "query": """Click on the search bar 'Type here to search...', type 'selenium', and press the 'Enter' key""",
        "example": """
        <body>
            <h1>Search Page Example</h1>
            <input id="searchBar" type="text" placeholder="Type here to search...">
            <button id="searchButton">Search</button>
            <script>
                document.getElementById('searchButton').onclick = function() {{
                    var searchText = document.getElementById('searchBar').value;
                    alert("Searching for: " + searchText);
                }};
            </script>
        </body>

        Query: Click on the search bar 'Type here to search...', type 'selenium', and press the 'Enter' key

        Completion:
        ```javascript
        // First, let's select the search bar using its ID.
        const searchBar = document.querySelector('#searchBar');

        // Simulate a click action on the search bar.
        searchBar.click();

        // Now, we can simulate typing 'selenium' into the search bar.
        searchBar.value = 'selenium';

        // To simulate pressing the 'Enter' key, we create a new event for the 'Enter' key and dispatch it.
        const enterKeyEvent = new KeyboardEvent('keypress', {{'key': 'Enter'}});
        searchBar.dispatchEvent(enterKeyEvent);
        ```
        """,
    },
    {
        "query": """Click on the title Link 1 and then click on the title Link 2""",
        "example": """
        HTML:

        <body>
            <h1>Welcome to the Mock Page</h1>
            <div id="links">
                <a href="#link1" id="link1">Link 1</a>
                <br>
                <a href="#link2" class="link">Link 2</a>
                <br>
            </div>
        </body>

        Query: Click on the title Link 1 and then click on the title Link 2

        Completion:
        ```javascript
        // To click on Link 1, we select it by its ID and simulate a click.
        document.querySelector('#link1').click();

        // Next, to click on Link 2, we select it by its class name and simulate a click.
        document.querySelector('.link').click();
        ```
    """,
    },
    {
        "query": "Select the text inside the third paragraph",
        "example": """
        HTML:

<body>
    <p id="para1">This is the first paragraph.</p>
    <p id="para2">This is the second paragraph.</p>
    <p id="para3">This is the third paragraph, which we will select and copy.</p>
    <p id="para4">This is the fourth paragraph.</p>
</body>

Query: Select the text inside the third paragraph

Completion:

```javascript
// To select the text of the third paragraph, we use its ID.
const para3 = document.querySelector('#para3');
const range = document.createRange();
const selection = window.getSelection();

// Clear any previous selections
selection.removeAllRanges();

// Select the paragraph's text
range.selectNodeContents(para3);
selection.addRange(range);
```
""",
    },
    {
        "query": """Fill out the registration form with the username 'new_user' and password 'securepassword123'""",
        "example": """
        HTML:

        <body>
            <form id="registrationForm">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <button type="submit">Register</button>
            </form>
        </body>

        Query: Fill out the registration form with the username 'new_user' and password 'securepassword123'

        ```javascript
        // Function to fill out and submit the registration form
        function submitRegistrationForm(username, password) {{
            // Select the username and password input fields
            const usernameInput = document.querySelector('#username');
            const passwordInput = document.querySelector('#password');

            // Check if both input fields are found
            if (!usernameInput || !passwordInput) {{
                console.error('Input fields not found');
                return;
            }}

            // Set the input values
            usernameInput.value = username;
            passwordInput.value = password;

            // Find and submit the form
            const form = document.querySelector('#registrationForm');
            if (form) {{
                form.submit();
            }} else {{
                console.error('Registration form not found');
            }}
        }}

        // Example usage
        submitRegistrationForm('new_user', 'securepassword123');
        ```
        """,
    },
    {
        "query": """Select the option 'Blue' from the dropdown menu and click the submit button""",
        "example": """
                HTML:

        <body>
            <label for="favoriteColor">Choose your favorite color:</label>
            <select id="favoriteColor" name="favoriteColor">
                <option value="red">Red</option>
                <option value="blue">Blue</option>
                <option value="green">Green</option>
                <option value="yellow">Yellow</option>
            </select>
            <button id="submitColor">Submit</button>
        </body>

        Query:  Select the option 'Blue' from the dropdown menu and click the submit button

        ```javascript
        // Function to select a favorite color and submit the survey form
        function submitFavoriteColor(color) {{
            // Select the dropdown element by its ID
            var colorDropdown = document.querySelector('#favoriteColor');
            // Select the submit button by its ID
            var submitButton = document.querySelector('#submitColor');

            // Set the value of the dropdown to the desired color
            colorDropdown.value = color;

            // Check if the selected color option exists
            if (colorDropdown.value !== color) {{
                console.error('Color option not found:', color);
                return;
            }}

            // Submit the survey by clicking the submit button
            // This action could vary depending on how the survey is processed
            submitButton.click();
        }}
        // Example usage
        submitFavoriteColor('blue');
        ```
""",
    },
    {
        "query": """Select the option 'Motorcycle' from the dropdown menu and click the submit button.""",
        "example": """
        HTML:
        <body>
            <label for="vehicleChoice">Select your vehicle type:</label>
            <select id="vehicleChoice" name="vehicleChoice">
                <option value="car">Car</option>
                <option value="truck">Truck</option>
                <option value="motorcycle">Motorcycle</option>
                <option value="bicycle">Bicycle</option>
            </select>
            <button id="submitVehicle">Submit Vehicle Type</button>
        </body>
        
        Query: Select the option 'Motorcycle' from the dropdown menu and click the submit button.
        
        Completion:
        ```javascript
        // Function to select a vehicle type and submit the form
        function submitVehicleType(type) {{
            // Access the dropdown element by its ID
            var vehicleDropdown = document.getElementById('vehicleChoice');
            // Access the submit button by its ID
            var submitButton = document.getElementById('submitVehicle');

            // Attempt to set the dropdown value to the specified type
            vehicleDropdown.value = type;

            // Verify the selected value
            if (vehicleDropdown.value !== type) {{
                console.error('Vehicle type not available:', type);
                return;
            }}

            // Simulate form submission by clicking the submit button
            submitButton.click();
        }}

        // Example usage
        submitVehicleType('motorcycle');
        """,
    },
    {
        "query": """Select the option 'Cherry' from the dropdown menu and click the submit button.""",
        "example": """
        HTML:
        <body>
            <label for="fruitChoice">Choose a fruit:</label>
            <select id="fruitChoice" name="fruitChoice">
                <option value="apple">Apple</option>
                <option value="banana">Banana</option>
                <option value="cherry">Cherry</option>
                <option value="date">Date</option>
            </select>
            <button id="submitFruit">Submit Choice</button>
        </body>
        
        Query: Select the option 'Cherry' from the dropdown menu and click the submit button.
        
        Completion:
        ```javascript
        // Function to select a fruit and submit the form
        function submitFruitSelection(fruit) {{
            // Get the dropdown element and the submit button by their IDs
            var fruitDropdown = document.getElementById('fruitChoice');
            var submitButton = document.getElementById('submitFruit');

            // Set the dropdown to the desired fruit
            fruitDropdown.value = fruit;

            // Check if the selected fruit option is actually set
            if (fruitDropdown.value !== fruit) {{
                console.error('Fruit option not found:', fruit);
                return;
            }}

            // Submit the choice by clicking the submit button
            submitButton.click();
        }}

        // Example usage
        submitFruitSelection('cherry');
        ```
        """,
    },
    {
        "query": "Select the radio button for a rating of '4' and submit the form.",
        "example": """
        HTML:
        <body>
            <label for="rating">Rate our service:</label>
            <form id="serviceRating">
                <input type="radio" id="rate1" name="rating" value="1"><label for="rate1">1</label>
                <input type="radio" id="rate2" name="rating" value="2"><label for="rate2">2</label>
                <input type="radio" id="rate3" name="rating" value="3"><label for="rate3">3</label>
                <input type="radio" id="rate4" name="rating" value="4"><label for="rate4">4</label>
                <input type="radio" id="rate5" name="rating" value="5"><label for="rate5">5</label>
                <button type="submit">Submit Rating</button>
            </form>
        </body>
        
        Query: Select the radio button for a rating of '4' and submit the form.

        ```javascript
        // Function to select a rating and submit the form
        function submitServiceRating(rating) {{
            // Check if the rating is within the acceptable range
            if (rating < 1 || rating > 5) {{
                console.error('Rating must be between 1 and 5');
                return;
            }}

            // Get the radio button for the specified rating
            var radioButton = document.getElementById('rate' + rating);
            radioButton.checked = true;

            // Submit the form
            document.getElementById('serviceRating').submit();
        }}

        // Example usage
        submitServiceRating(4);
        ```
        """,
    },
    {
        "query": "Enter the email address 'user@example.com' into the email input field and click the subscribe button.",
        "example": """
        <body>
            <h2>Subscribe to our Newsletter</h2>
            <form id="newsletterForm">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" placeholder="Enter your email">
                <button type="submit">Subscribe</button>
            </form>
        </body>
        
        Query: Enter the email address user@example.com into the email input field and click the subscribe button.
        
        Completion:
        ```javascript
        // Function to submit an email address for newsletter subscription
        function subscribeToNewsletter(email) {{
            // Get the email input element by its ID
            var emailInput = document.getElementById('email');

            // Set the email value
            emailInput.value = email;

            // Validate the email format (simple validation)
            if (!email.includes('@')) {{
                console.error('Invalid email address');
                return;
            }}

            // Submit the form
            document.getElementById('newsletterForm').submit();
        }}

        // Example usage
        subscribeToNewsletter('user@example.com');
        ```
        """,
    },
]

plain_selenium_few_shot = """
    Your objective is to craft Selenium Python code snippets to fulfill specific actions on a web page. 
Your solutions must be encapsulated in Python code cells, considering external web resources and libraries as accessible. 
Pay close attention to the uniqueness of attribute values when targeting elements on the page. Where possible, employ a blend of text content, class names, or IDs for a more precise element targeting strategy. 
In scenarios where multiple elements share similar functions, prioritize accuracy by selecting the most relevant element. 
Utilize the contains@class syntax for targeting elements with multiple classes.

Prior to writing your code, assume the initial setup below has already been executed:
```python
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
```
{examples}

---

HTML:
{context_str}
Query: {query_str}
Completion:
"""

plain_js_few_shot = """

Your mission is to develop JavaScript code snippets capable of performing specified tasks on web pages. Ensure your responses are structured strictly as JavaScript code. Consideration for external web resources and libraries is permitted and encouraged to enhance functionality or streamline solutions.

When engaging with DOM elements, avoid making assumptions about the uniqueness of attribute values. Instead, refine your selection criteria by leveraging a mix of text content, class names, or IDs. This approach aids in accurately pinpointing the desired element amidst potential duplicates. In scenarios where numerous elements share similar functionalities, execute due diligence to identify and interact with the element most closely aligned with the task's requirements.

Emphasize the utilization of querySelector and querySelectorAll for DOM manipulation. These methods provide a robust framework for element selection, accommodating complex selectors that can combine attribute values, class names, and pseudo-classes, among other criteria.

You can assume the following code has been executed:
```javascript
document.addEventListener('DOMContentLoaded', (event) => {{
    console.log('DOM fully loaded and parsed');
}});
```

{examples}

---

HTML:
{context_str}
Query: {query_str}
Completion:

"""
