/* This is test class to test flagger built */

//author: Stefan Mitchell

class testFlagger {

    public static void main(String[] args) {

        Flagger F1 = new Flagger(2, 0);

        System.out.println(F1.flagged());
        System.out.println(F1.getrate());
        System.out.println(F1.getstatus());
        F1.setstatus(1);
        F1.getstatus();
    }

}
