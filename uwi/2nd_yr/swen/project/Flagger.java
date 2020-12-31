import java.util.*;

public class Flagger {

    // Attributes of flagger
    final int Maxrate = 5;
    int rate;
    int status;
    boolean flagged;
    Scanner scanner = new Scanner(System.in);

    // flagger constructor

    public Flagger(int rating, int status) {

        if (status == 0 || status == 1) {
            this.status = status;
        }

        else {

            System.out.println("Invalid status entered");
            System.out.println(" valid statuses:'0' for a new business or '1' for an existing business");
            System.out.println("Exitting....");
            System.exit(-1);
        }

        rate = rating;

    }

    // allows admins to change current status of business from new (0) to existing
    // (1) or vice versa
    public void setstatus(int stat) {

        if (stat == 0) {
            System.out.println(" Business status:New business");
            status = stat;
        }

        else if (stat == 1) {

            System.out.println(" Business status:existing business");
            status = stat;

        }

        else if (stat != 0 || stat != 1) {
            System.out.println("Invalid status entered");
            System.out.println("Please enter a valid status,'0' for a new business or '1' for an existing business:");
            int i = scanner.nextInt();
            System.out.println("response: " + i);

            while (i != 0 || i != 1) {

                System.out.println("Invalid status entered");
                System.out.println(
                        "Please enter a valid status,'0' for a new business or '1' for an existing business:" + i);
                System.out.println("response: " + i);
                setstatus(i);
            }

        }

        System.out.println("status set");

    }

    // allows admins to check current status of business

    public int getstatus() {

        if (status == 1)

        {
            System.out.println("current status:Existing Business");

        }

        else {
            System.out.println("current status:New Business");
        }

        return status;

    }

    /// gets current rating of business
    public int getrate() {

        return rate;

    }

    /// shows if business is flagged or not

    public String flagged() {

        String flag_status = "";
        boolean flagged = false;

        if (getstatus() == 1 && getrate() > 3 && getrate() < Maxrate) {
            System.out.println("Existing Business detected");
            flagged = false;
            flag_status = "No";

        }

        else if (getstatus() == 1 && getrate() < 3 && getrate() < Maxrate) {

            System.out.println("Existing Business detected");
            flagged = true;
            flag_status = "Yes";

        }

        else {

            System.out.println("New Business detected");
            flagged = false;
            flag_status = "No";

        }

        return ("flagged:" + flag_status);
    }

}