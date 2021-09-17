import { Injectable } from '@angular/core';
import { Storage } from '@ionic/storage';

export interface SessionLog {
  id:string,
  email:string,
  token:string,
  role:string
}

const SESSION_LOG = 'info_session';

const API_URL = 'http://ciloop.co/api-futbolflex/public';

@Injectable({
  providedIn: 'root'
})
export class StorageService {

  constructor(private storage: Storage) { }

  getApiUrl(){
    return API_URL;
  }

  addSessionLog(sessionLog: SessionLog): Promise<any> {

    return this.storage.get(SESSION_LOG).then((sessionLogs: SessionLog[]) => {
      if (sessionLogs) {
        sessionLogs.push(sessionLog);
        return this.storage.set(SESSION_LOG, sessionLogs)
      } else {
        return this.storage.set(SESSION_LOG, [sessionLog]);
      }
    });

  }

  getSessionLog(): Promise<SessionLog[]>{
    return this.storage.get(SESSION_LOG);
  }

  updateSessionLog(sessionLog: SessionLog): Promise<any>{
    return this.storage.get(SESSION_LOG).then((sessionLogs: SessionLog[]) => {
      if (!sessionLogs || sessionLogs.length === 0) {
        return this.storage.get(SESSION_LOG).then((sessionLogs: SessionLog[]) => {
          if (sessionLogs) {
            sessionLogs.push(sessionLog);
            return this.storage.set(SESSION_LOG, sessionLogs)
          } else {
            return this.storage.set(SESSION_LOG, [sessionLog]);
          }
        });
      }

      let newSessionLogs: SessionLog[] = [];

      for (let i of sessionLogs) {
        if (i.email === sessionLog.email) {
          newSessionLogs.push(sessionLog);
        } else {
          newSessionLogs.push(i);
        }
      }

      return this.storage.set(SESSION_LOG, newSessionLogs);
    });

  }

  deletSessionLog(email:string): Promise<SessionLog> {
    return this.storage.get(SESSION_LOG).then((sessionLogs: SessionLog[]) => {
      if (!sessionLogs || sessionLogs.length === 0) {
        return null;
      }

      let toKeep: SessionLog[] = [];

      for (let i of sessionLogs) {
        if (i.email !== email) {
          toKeep.push(i);
        }
      }
      return this.storage.set(SESSION_LOG, toKeep);

    });
  }
}

