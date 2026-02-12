import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;

public class SubmittheformwithvalidinputsTest {
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
    public void Submit_the_form_with_valid_inputs() {
        // Step: Click the submit button
        // TODO: Add assertions based on expected result
    }
}
