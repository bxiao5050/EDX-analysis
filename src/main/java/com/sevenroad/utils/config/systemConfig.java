package com.sevenroad.utils.config;

/**
 * Created by linlin.zhang on 2016/10/18.
 */
public class systemConfig {
    private static dataBaseConfig dbConfig;
    private static dataViewConfig dataViewConfig;
    private static String filePath = systemConfig.class.getClassLoader().getResource("").getPath()+"config.properties";

    private static otherConfig otherConfig;
    public static dataBaseConfig getDBConfig() {
        if(dbConfig == null) dbConfig = new dataBaseConfig();
        if (dbConfig.isloaded()) {
            return dbConfig;
        } else{
            dbConfig.load(filePath);
        }
        return dbConfig;
    }
    public static dataViewConfig getDataViewConfig(){
        if(dataViewConfig == null) dataViewConfig = new dataViewConfig();
        if (dataViewConfig.isloaded()) {
            return dataViewConfig;
        } else{
            dataViewConfig.load(filePath);
        }
        return dataViewConfig;
    }
    public static otherConfig getOtherConfig(){
        if(otherConfig == null) otherConfig = new otherConfig();
        if (otherConfig.isloaded()) {
            return otherConfig;
        } else{
            otherConfig.load(filePath);
        }
        return otherConfig;
    }
    public static void reload(){
        dbConfig.load(filePath);
        dataViewConfig.load(filePath);
        otherConfig.load(filePath);
    }
}
