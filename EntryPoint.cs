using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System.Threading;

class EntryPoint
{
    public static void VisibilityPrint(IWebElement thingy, string desc)
    {
        if (thingy.Displayed)
        {
            System.Console.ForegroundColor = System.ConsoleColor.Green;
            System.Console.WriteLine("OK! The '{0}' box is visible!", desc);
            System.Console.ForegroundColor = System.ConsoleColor.White;
        }
        else
        {
            System.Console.ForegroundColor = System.ConsoleColor.Red;
            System.Console.WriteLine("ERROR! Failed to locate the '{0}'!.", desc);
            System.Console.ForegroundColor = System.ConsoleColor.White;
        }
    }

    public static void RunTest(string testText)
    {
        //initialize drivers
        IWebDriver driver = new ChromeDriver();
        IAlert alert;

        //go to page
        driver.Navigate().GoToUrl("C:\\Users\\Eibzz\\Desktop\\Code\\f16-deploy-Eibzz-master\\f16-deploy-Eibzz-master\\client.html");

        //wait for alert to pop up
        Thread.Sleep(1000);

        //"Get that annoying 'ALERT!!!!!' word box trying to get my attention outta here. 
        // No way that's of any importance or anything, RIGHT??!" -Users probably (2017)
        alert = driver.SwitchTo().Alert();
        alert.Accept();

        //can we see the email input box?
        IWebElement elmLoginEmail = driver.FindElement(By.Id("login-email"));
        VisibilityPrint(elmLoginEmail, "Login Email");

        //how about the password input box?
        IWebElement elmLoginPassword = driver.FindElement(By.Id("login-password"));
        VisibilityPrint(elmLoginPassword, "Login Password");

        //submit button's probably there too, but better safe than sorry
        IWebElement elmLoginSubmit = driver.FindElement(By.Id("input-login"));
        VisibilityPrint(elmLoginSubmit, "Login Button");

        //input test information and 'click' the submit button
        elmLoginEmail.SendKeys("test@test.com");
        elmLoginPassword.SendKeys("test");
        elmLoginSubmit.Click();

        Thread.Sleep(1000);

        //find the message box and print if we found it
        IWebElement elmMessageBox = driver.FindElement(By.Id("message"));
        VisibilityPrint(elmMessageBox, "Message Box");

        //put a message in the message box
        //System.Random rando = new System.Random();
        //int r = rando.Next(1024);
        //string msg = string.Format("Message: {0}", testText);
        elmMessageBox.SendKeys(testText);

        //find the submit message button and print if we found it
        IWebElement elmSendButton = driver.FindElement(By.Id("send-message"));
        VisibilityPrint(elmSendButton, "Send Message Button");

        elmSendButton.Click();

        Thread.Sleep(1000);

        driver.Quit();
    }

    static void Main(string[] args)
    {
        string tt = args[0];
        System.Console.WriteLine(tt);
        //tt = tt.Replace('_', ' ');
        //System.Console.WriteLine(tt);
        //for(int i = 0; i<10; i++)
        //{
        //    RunTest();
        //    Thread.Sleep(1000);
        //}
        RunTest(tt);
    }
}
