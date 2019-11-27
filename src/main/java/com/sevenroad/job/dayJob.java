package com.sevenroad.job;

import com.sevenroad.dao.connection.SystemConnection;
import com.sevenroad.dao.data.jobItem;
import com.sevenroad.job.task.fiveMinTask;
import com.sevenroad.singleton.CacheSigleton;
import com.sevenroad.utils.Logger;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

import java.util.LinkedList;

/**
 * Created by linlin.zhang on 2017/1/6.
 */
public class dayJob implements Job {
    public static final  int DAY = 86400000;
    public void execute(JobExecutionContext jobExecutionContext) throws JobExecutionException {
        CacheSigleton.getQueryResultCache().clearCache();
        SystemConnection conn = new SystemConnection();
        try {
            LinkedList<jobItem> jobs = conn.getJob();
            for(int i = 0;i<jobs.size();i++){
                jobItem job = jobs.get(i);
                if(job.getInterval() == DAY){
                    jobWork.getThreadPool().execute(new fiveMinTask(job));
                }
            }
        }
        catch (Exception ex){
            Logger.getInstance().Error(ex);
        }
    }
}
