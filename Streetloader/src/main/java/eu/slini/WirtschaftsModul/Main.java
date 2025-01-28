package eu.slini.WirtschaftsModul;

import org.json.JSONArray;
import org.json.JSONObject;


import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        //Leipzig
        String overpassUrl = "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3Barea%5B%22de%3Aamtlicher_gemeindeschluessel%22%3D14713000%5D-%3E.a%3B%28way%5B%22highway%22%5D%28area.a%29%3B%29%3Bout%3B";

//Augsburg
      //  String overpassUrl = "https://overpass-api.de/api/interpreter?data=%5Bout%3Ajson%5D%3Barea%5B%22de%3Aamtlicher_gemeindeschluessel%22%3D09761000%5D-%3E.a%3B%28way%5B%22highway%22%5D%28area.a%29%3B%29%3Bout%3B\n";
        DBCon DBCon = new DBCon();

        try {
            URL url = new URL(overpassUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("GET");

            Scanner scanner = new Scanner(new InputStreamReader(connection.getInputStream()));
            StringBuilder response = new StringBuilder();
            while (scanner.hasNext()) {
                response.append(scanner.nextLine());
            }
            scanner.close();

            JSONObject jsonResponse = new JSONObject(response.toString());
            JSONArray elements = jsonResponse.getJSONArray("elements");


            for (int i = 0; i < elements.length(); i++) {
                JSONObject element = elements.getJSONObject(i);
                int ID = element.getInt("id");
                if (element.has("tags")) {
                    JSONObject tags = element.getJSONObject("tags");

                    String name = tags.optString("name", "Unbenannt");
                    String ref = tags.optString("ref", "Unbenannt");
                    String highway = tags.optString("highway", "Unbenannt");
                    String surface = tags.optString("surface", "Unbekannt");
                    String smoothness = tags.optString("smoothness", "Unbenannt");
                    String maxspeed = tags.optString("maxspeed", "9999");
                    String lanes = tags.optString("lanes", "9999");
                    String sidewalk = tags.optString("sidewalk", "Unbenannt");
                    String cycleway = tags.optString("cycleway", "Unbekannt");
                    String bicycle = tags.optString("bicycle", "Unbenannt");
                    String hazard = tags.optString("hazard", "Unbenannt");
                    String width = tags.optString("width", "9999.99");

                    Strasse street = new Strasse(ID,name,ref,highway,surface,smoothness,maxspeed,lanes,sidewalk,cycleway,bicycle,hazard,width);
                    DBCon.writeDB(street);
                    System.out.println(i +":"+ street.toString());
                }
            }

            System.out.println("DONE!");

        } catch (IOException e) {
            System.err.println("Fehler beim Abrufen der Daten: " + e.getMessage());
        }


    }
}