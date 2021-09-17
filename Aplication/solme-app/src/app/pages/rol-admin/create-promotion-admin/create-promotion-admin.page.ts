import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { StorageService, SessionLog } from 'src/app/services/storage.service';

@Component({
  selector: 'app-create-promotion-admin',
  templateUrl: './create-promotion-admin.page.html',
  styleUrls: ['./create-promotion-admin.page.scss'],
})
export class CreatePromotionAdminPage implements OnInit {

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  id:string;
  email:string;
  password:string;
  tableros:object;
  token: string;
  role: string;
  usuario: string;

  headers: HttpHeaders;

  respuesta:object;

  device_type: string;
  device_name: string;
  device_description: string;
  device_code: string;

  constructor(private storageService: StorageService, private router: Router, private http: HttpClient) { }

  ngOnInit() {
  }

  goPromotionsAdmin(){
    this.router.navigate(['/tabs-admin/promotions-admin'])
  }

  AddTablero(){
    console.log('Estas intentando añadir un tablero')



    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.headers = new HttpHeaders({
        "Authorization":"Bearer " + this.token,
        "Content-Type" : "aplication/json"
      });

      let postData = {
        "device_type": this.device_type,
        "device_name": this.device_name,
        "device_description": this.device_description,
        "device_code": this.device_code,
      }

      let api_url = this.storageService.getApiUrl();

      this.http.post(api_url + '/api/crear-tablero', postData, {headers: this.headers})
    .subscribe(data => {
      console.log(data);
      this.respuesta = data;
    });
    });
    this.router.navigate(['/tabs-admin/promotions-admin'])
  }
}
