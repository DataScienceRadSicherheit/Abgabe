package eu.slini.WirtschaftsModul;

import java.sql.*;

public class DBCon {

    Connection conn;
    static String sql = "INSERT INTO \"street\" (ID, name, ref, highway, surface, smoothness, maxspeed, lanes, sidewalk, cycleway, bicycle, hazard, width) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

    public DBCon(){

        String url = "jdbc:postgresql://192.168.2.13:5432/Datascience";
        String user = "user";
        String password = "user";

        try {
            conn = DriverManager.getConnection(url, user, password);
        } catch (SQLException e) {
            System.out.println("Verbindung zu DB Fehlgeschlagen");
            throw new RuntimeException(e);
        }
    }

    public void writeDB(Strasse street){

        try {
            PreparedStatement pstmt = conn.prepareStatement(sql);

            pstmt.setString(1, ""+street.getID());
            pstmt.setString(2, street.getName());
            pstmt.setString(3, street.getRef());
            pstmt.setString(4, street.getHighway());
            pstmt.setString(5, street.getSurface());
            pstmt.setString(6, street.getSmoothness());
            pstmt.setString(7, street.getMaxspeed());
            pstmt.setString(8, street.getLanes());
            pstmt.setString(9, street.getSidewalk());
            pstmt.setString(10, street.getCycleway());
            pstmt.setString(11, street.getBicycle());
            pstmt.setString(12, street.getHazard());
            pstmt.setString(13, street.getWidth());

            pstmt.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
