package eu.slini.WirtschaftsModul;

public class Strasse {

    private int ID;

    private String name;
    private String ref;
    private String highway; //Typ
    private String surface;
    private String smoothness;
    private String maxspeed;
    private String lanes;
    private String sidewalk;
    private String cycleway;
    private String bicycle;
    private String hazard;
    private String width;
    private String plz;

    public Strasse(){

    }

    public Strasse(int ID, String name, String ref, String highway, String surface, String smoothness, String maxspeed, String lanes, String sidewalk, String cycleway, String bicycle, String hazard, String width) {
        this.ID = ID;
        this.name = name;
        this.ref = ref;
        this.highway = highway;
        this.surface = surface;
        this.smoothness = smoothness;
        this.maxspeed = maxspeed;
        this.lanes = lanes;
        this.sidewalk = sidewalk;
        this.cycleway = cycleway;
        this.bicycle = bicycle;
        this.hazard = hazard;
        this.width = width;

    }

    public String getWidth() {
        return width;
    }

    public void setWidth(String width) {
        this.width = width;
    }

    public int getID() {
        return ID;
    }

    public String getPlz() {
        return plz;
    }

    public String getName() {
        return name;
    }

    public String getRef() {
        return ref;
    }

    public String getHighway() {
        return highway;
    }

    public String getSurface() {
        return surface;
    }

    public String getSmoothness() {
        return smoothness;
    }

    public String getMaxspeed() {
        return maxspeed;
    }

    public String getLanes() {
        return lanes;
    }

    public String getSidewalk() {
        return sidewalk;
    }

    public String getCycleway() {
        return cycleway;
    }

    public String getBicycle() {
        return bicycle;
    }

    public String getHazard() {
        return hazard;
    }

    public void setID(int ID) {
        this.ID = ID;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setRef(String ref) {
        this.ref = ref;
    }

    public void setHighway(String highway) {
        this.highway = highway;
    }

    public void setSurface(String surface) {
        this.surface = surface;
    }

    public void setSmoothness(String smoothness) {
        this.smoothness = smoothness;
    }

    public void setMaxspeed(String maxspeed) {
        this.maxspeed = maxspeed;
    }

    public void setLanes(String lanes) {
        this.lanes = lanes;
    }

    public void setSidewalk(String sidewalk) {
        this.sidewalk = sidewalk;
    }

    public void setCycleway(String cycleway) {
        this.cycleway = cycleway;
    }

    public void setBicycle(String bicycle) {
        this.bicycle = bicycle;
    }

    public void setHazard(String hazard) {
        this.hazard = hazard;
    }

    @Override
    public String toString() {
        return "Strasse{" +
                "ID='" + ID + '\'' +
                ", name='" + name + '\'' +
                ", ref='" + ref + '\'' +
                ", highway='" + highway + '\'' +
                ", surface='" + surface + '\'' +
                ", smoothness='" + smoothness + '\'' +
                ", maxspeed=" + maxspeed +
                ", lanes=" + lanes +
                ", sidewalk='" + sidewalk + '\'' +
                ", cycleway='" + cycleway + '\'' +
                ", bicycle='" + bicycle + '\'' +
                ", hazard='" + hazard + '\'' +
                ", width=" + width +
                '}';
    }
}
