import org.junit.jupiter.api.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;

public class VerifyusernamefieldacceptsonlyalphanumericcharactersTest {
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
    public void Verify_username_field_accepts_only_alphanumeric_characters() {
        // Step: Enter alphanumeric characters in username input
        // TODO: Add assertions based on expected result
    }
}
