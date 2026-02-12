import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;

public class VerifyformdoesnotallowHTMLorscriptinjectioninusernameandpasswordfieldsTest {
    private WebDriver driver;
    private DefaultpagePage page;

    @BeforeEach
    public void setUp() {
        driver = new ChromeDriver();
        page = new DefaultpagePage(driver);
    }

    @AfterEach
    public void tearDown() {
        driver.quit();
    }

    @Test
    public void Verify_form_does_not_allow_HTML_or_script_injection_in_username_and_password_fields() {
        // Step: Enter HTML tags or JavaScript code in username and password fields
        // Step: Click submit button
        // TODO: Add assertions based on expected result
    }
}
