import java.util.*;
import java.lang.*;
import java.io.*;

/**
 * @author dara-kaye
 *
 */
public class Database {

    final static int LENGTH_OF_DATABASE = 5; // Length of Database array

    static String rank;
    static Database[] database = new Database[LENGTH_OF_DATABASE];
    static ArrayList<Database> list = new ArrayList<Database>();
    static Object[] scoreList = new Object[LENGTH_OF_DATABASE];
    static String businessOwner;
    static String businessName;
    static String businessType;
    static String businessLocation;
    static String businessContact;

    static int businessRate;

    ArrayList<String> businessNames = new ArrayList<String>(); // Create an ArrayList object with the name of each
                                                               // business
    ArrayList<String> noRank = new ArrayList<String>(); // ArrayList object for all business with no rating
    ArrayList<String> rankOne = new ArrayList<String>(); // ArrayList object with the name of each business
    ArrayList<String> rankTwo = new ArrayList<String>(); // Create an ArrayList object with the name of each business
    ArrayList<String> rankThree = new ArrayList<String>(); // Create an ArrayList object with the name of each business
    ArrayList<String> rankFour = new ArrayList<String>(); // Create an ArrayList object with the name of each business
    ArrayList<String> rankFive = new ArrayList<String>(); // Create an ArrayList object with the name of each business

    for(
    int i = 0;i<database.size();i++)
    {
        database.add(i[1]); // Here I wanted to make a list with just the name of each business that are
                            // present in the database. I expect that its the name of each business that
                            // would be used whenever they're listed/advertised/put in any order
                            // It probably would use like a getBusinessName method from When each entry was
                            // being made
        for (String s : businessNames) {
            if (businessRate == 1) {
                rankOne.add(s);
            } else if (businessRate == 2) {
                rankTwo.add(s);
            } else if (businessRate == 3) {
                rankThree.add(s);
            } else if (businessRate == 4) {
                rankFour.add(s);
            } else if (businessRate == 5) {
                rankFive.add(s);
            } else {
                noRank.add(s);
            }
        } // Since the rating a business receives would affect its rank, I was grouping
          // them by rating first, sort them in that group and then when ranking print the
          // groups in a particular order.
          // Would another getter be used here to retrieve the rating that's already
          // assigned to each business

        for (int i = 0; i < rankOne.size(); i++) {
            int countA = 0;
            rank = "A" + countA + 1;
            countA++;
        }
        for (int i = 0; i < rankTwo.size(); i++) {
            int countB = 0;
            rank = "B" + countB + 1;
            countB++;
        }
        for (int i = 0; i < rankThree.size(); i++) {
            int countC = 0;
            rank = "C" + countC + 1;
            countC++;
        }
        for (int i = 0; i < rankFour.size(); i++) {
            int countD = 0;
            rank = "D" + countD + 1;
            countD++;
        }
        for (int i = 0; i < rankFive.size(); i++) {
            int countE = 0;
            rank = "E" + countE + 1;
            countE++;
        }
        for (int i = 0; i < noRank.size(); i++) {
            int countZ = 0;
            rank = "Z" + countZ + 1;
            countZ++;
        }
    }
}}