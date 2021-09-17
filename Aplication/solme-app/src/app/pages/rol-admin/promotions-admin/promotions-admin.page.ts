import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StorageService, SessionLog } from 'src/app/services/storage.service';
import { ActivatedRoute } from '@angular/router';
import { AlertController } from '@ionic/angular';
import {HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-promotions-admin',
  templateUrl: './promotions-admin.page.html',
  styleUrls: ['./promotions-admin.page.scss'],
})
export class PromotionsAdminPage implements OnInit {

  headers: HttpHeaders;

  id:string;
  email:string;
  password:string;
  tableros:object;
  token: string;
  role: string;

  users_aproved:object;
  users_rejected:object;
  users_waiting:object;

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  constructor(private http: HttpClient, private router: Router, public alertController: AlertController, private storageService: StorageService, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    this.loadTableros();
  }

  loadTableros(){
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.getTableros(this.token).subscribe(data => {
        this.tableros = data;
        console.log(this.tableros);
      });
    });
  }


  goCreatePromotion(){
    this.router.navigate(['/create-promotion-admin'])
  }

  goInfoPromotion(tablero){
    this.router.navigate(['/info-product-admin'], tablero)
  }
  goProfileAdmin(){
    this.router.navigate(['/profile-admin'])
  }

  //Listar tableros
  getTableros(token:string) {

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.get<any>(api_url + '/api/listar-tableros', {headers: this.headers});
  }

  goCrearTablero(){
    this.router.navigate(['/create-promotion-admin'])
  }
}
