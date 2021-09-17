import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SessionLog, StorageService } from 'src/app/services/storage.service';

@Component({
  selector: 'app-profile-admin',
  templateUrl: './profile-admin.page.html',
  styleUrls: ['./profile-admin.page.scss'],
})
export class ProfileAdminPage implements OnInit {

  constructor(private storageService: StorageService, private router: Router, private http: HttpClient) { }
  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  id: string;
  token: string;
  email: string;

  headers: HttpHeaders;
  
  usuariodata={
    id_admin: null,
    name: null,
    last_name: null,
    email: null,
    address: null,
    phone_number: null,
    born_date: null,
    favorite_flavor: null,
  };

  ngOnInit() {
    this.loadSessionLog();
    // console.log(this.usuariodata);
    
  }

  loadSessionLog(){
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.email = i.email;
        this.token = i.token;
      }
      // console.log(this.id);
      // console.log(this.email);
      // console.log(this.token);

      this.headers = new HttpHeaders({
        "Authorization":"Bearer " + this.token,
        "Content-Type" : "aplication/json"
      });

      let api_url = this.storageService.getApiUrl();

      this.http.get(api_url + '/api/user/' + this.id, {headers: this.headers})
      .subscribe(data => {
        // console.log(data)
        this.usuariodata['id_admin']=data['user']['id'];
        this.usuariodata['name']=data['user']['name'];
        this.usuariodata['last_name']=data['user']['last_name'];
        this.usuariodata['email']=data['user']['email'];
        this.usuariodata['address']=data['user']['address'];
        this.usuariodata['phone_number']=data['user']['phone_number'];
        this.usuariodata['born_date']=data['user']['born_date'];
        this.usuariodata['basic_profile']=data['user']['basic_profile'];
      });
    });
  }

  doCloseSession(){
    this.deleteSessionLog()
    this.router.navigate(['/login'])
  }

  deleteSessionLog(){
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.email = i.email;
        this.token = i.token;
      }
    this.storageService.deletSessionLog(this.email);
    });
  }
}
