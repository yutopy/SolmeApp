import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StorageService, SessionLog } from 'src/app/services/storage.service';
import { ActivatedRoute } from '@angular/router';
import { AlertController } from '@ionic/angular';
import {HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-promotions-user',
  templateUrl: './promotions-user.page.html',
  styleUrls: ['./promotions-user.page.scss'],
})
export class PromotionsUserPage implements OnInit {

  headers: HttpHeaders;

  id:string;
  email:string;
  password:string;
  metricas:object;
  token: string;
  role: string;

  users_aproved:object;
  users_rejected:object;
  users_waiting:object;

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  constructor(private http: HttpClient, private router: Router, public alertController: AlertController, private storageService: StorageService, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    //this.loadTablero();
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.getMetricas(this.token, this.id).subscribe(data => {
        this.metricas = data;
      });
    });
  } 

  //Listar metricas
  getMetricas(token:string, id:string) {

    let postData = {
      "user_id":id
    }

    let api_url = this.storageService.getApiUrl();

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });
    return this.http.post(api_url + '/api/listar-metricas', postData, {headers: this.headers});
  }

}