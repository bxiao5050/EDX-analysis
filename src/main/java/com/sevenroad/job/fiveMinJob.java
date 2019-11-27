package com.sevenroad.job;

import com.sevenroad.dao.connection.SystemConnection;
import com.sevenroad.dao.data.jobItem;
import com.sevenroad.job.task.fiveMinTask;
import com.sevenroad.utils.Logger;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;

import java.util.LinkedList;

/**
 * Created by linlin.zhang on 2017/1/4.
 */
public class fiveMinJob implements Job {
    public static final  int FIVE_MIN = 300000;
    @Override
    public void execute(JobExecutionContext jobExecutionContext) throws JobExecutionException {
        SystemConnection conn = new SystemConnection();
        try {
            LinkedList<jobItem> jobs = conn.getJob();
            for(int i = 0;i<jobs.size();i++){
                jobItem job = jobs.get(i);
                if(job.getInterval() == FIVE_MIN){
                    jobWork.getThreadPool().execute(new fiveMinTask(job));
                }
            }
        }
        catch (Exception ex){
            Logger.getInstance().Error(ex);
        }
    }
}
