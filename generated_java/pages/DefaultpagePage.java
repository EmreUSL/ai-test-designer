import org.openqa.selenium.*;
import org.openqa.selenium.support.*;

public class DefaultpagePage {
    private WebDriver driver;

    private WebElement _token;
    private WebElement username;
    private WebElement password;
    private WebElement None;
    private WebElement None;
    private WebElement None;
    private WebElement None;
    private WebElement None;
    private WebElement None;

    public DefaultpagePage(WebDriver driver) {
        this.driver = driver;
        this._token = driver.findElement(By.name("_token"));
        this.username = driver.findElement(By.name("username"));
        this.password = driver.findElement(By.name("password"));
        this.None = driver.findElement(By.className("oxd-button"));
        this.None = driver.findElement(By.tagName("a"));
        this.None = driver.findElement(By.tagName("a"));
        this.None = driver.findElement(By.tagName("a"));
        this.None = driver.findElement(By.tagName("a"));
        this.None = driver.findElement(By.tagName("a"));
    }

    public void NONE__token(String value) {
    }

    public void SEND_KEYS_username(String value) {
    }

    public void SEND_KEYS_password(String value) {
    }

    public void CLICK_None(String value) {
    }

    public void CLICK_None(String value) {
    }

    public void CLICK_None(String value) {
    }

    public void CLICK_None(String value) {
    }

    public void CLICK_None(String value) {
    }

    public void CLICK_None(String value) {
    }

}
