import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.*;


//findet am Meisten verwendetes Material pro Abschnitt
public class Skript {

    public static String findMostFrequentString(List<String> strings) {
        // Zählt das Vorkommen jedes Strings
        Map<String, Integer> frequencyMap = new HashMap<>();
        for (String s : strings) {
            frequencyMap.put(s, frequencyMap.getOrDefault(s, 0) + 1);
        }

        // Findet den maximalen Vorkommenswert
        int maxFrequency = Collections.max(frequencyMap.values());

        // Sammelt alle Strings mit der maximalen Häufigkeit
        List<String> candidates = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : frequencyMap.entrySet()) {
            if (entry.getValue() == maxFrequency) {
                candidates.add(entry.getKey());
            }
        }

        // Wählt zufällig einen String aus, falls mehrere gleich häufig vorkommen
        Random random = new Random();
        return candidates.get(random.nextInt(candidates.size()));
    }


    public static void main (String[] args){

        String url = "jdbc:postgresql://192.168.2.13:5432/Wirtschaftsmodul";
        String user = "user";
        String password = "user";

        Connection conn;
        try {
            conn = DriverManager.getConnection(url, user, password);
        } catch (SQLException e) {
            System.out.println("Verbindung zu DB Fehlgeschlagen");
            throw new RuntimeException(e);
        }

        HashMap <String, ArrayList<String>> map = readCSV();

        System.out.println(map.size());

        for (String s : map.keySet()) {
            String mat = findMostFrequentString(map.get(s));
            writeDB(s,mat, conn);
        }

    }

    public static void writeDB(String id, String mat, Connection conn){

        String sql = "INSERT INTO \"dataLnew\" (id, surface) VALUES (?, ?)";

        PreparedStatement pstmt = null;
        try {
            pstmt = conn.prepareStatement(sql);

            pstmt.setString(1, id);
            pstmt.setString(2, mat);

            pstmt.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
        System.out.println(id + ": " + mat);
    }

    public static HashMap<String,ArrayList<String>> readCSV(){

        HashMap<String,ArrayList<String>> map = new HashMap<>();

        try (BufferedReader br = new BufferedReader(new FileReader("data.csv"))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.replace("\"", "");
             //   System.out.println(line);
                String[] values = line.split(",");
                String id = values[0];
                String mat1 = values[1];
                String mat2 = values[2];
                String mat3 = values[3];

                if (!id.equals("NULL")){
                    if (!mat1.equals("NULL")){
                        if (map.containsKey(id)){
                            map.get(id).add(mat1);
                        } else {
                            ArrayList<String> list = new ArrayList<>();
                            list.add(mat1);
                            map.put(id, list);
                        }
                    }
                    if (!mat2.equals("NULL")){
                        if (map.containsKey(id)){
                            map.get(id).add(mat2);
                        } else {
                            ArrayList<String> list = new ArrayList<>();
                            list.add(mat2);
                            map.put(id, list);
                        }
                    }
                    if (!mat3.equals("NULL")){
                        if (map.containsKey(id)){
                            map.get(id).add(mat3);
                        } else {
                            ArrayList<String> list = new ArrayList<>();
                            list.add(mat3);
                            map.put(id, list);
                        }
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return map;
    }

}
