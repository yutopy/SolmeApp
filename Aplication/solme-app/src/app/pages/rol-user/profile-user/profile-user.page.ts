import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SessionLog, StorageService } from 'src/app/services/storage.service';

@Component({
  selector: 'app-profile-user',
  templateUrl: './profile-user.page.html',
  styleUrls: ['./profile-user.page.scss'],
})
export class ProfileUserPage implements OnInit {

  constructor(private storageService: StorageService, private router: Router, private http: HttpClient) { }

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  id: string;
  token: string;
  email: string;

  headers: HttpHeaders;
  
  usuariodata={
    name: null,
    last_name: null,
    email: null,
    address: null,
    phone_number: null,
    favorite_flavor: null,
  };

  ngOnInit() {
    this.loadSessionLog();
  }

  goShoppingCart(){
    this.router.navigate(['/shopping-cart-user'])
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
        this.usuariodata['name']=data['user']['name'];
        this.usuariodata['last_name']=data['user']['last_name'];
        this.usuariodata['email']=data['user']['email'];
        this.usuariodata['address']=data['user']['address'];
        this.usuariodata['phone_number']=data['user']['phone_number'];
        this.usuariodata['favorite_flavor']=data['user']['favorite_flavor'];
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
