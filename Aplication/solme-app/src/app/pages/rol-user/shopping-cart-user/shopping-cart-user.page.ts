import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StorageService, SessionLog } from 'src/app/services/storage.service';
import { ActivatedRoute } from '@angular/router';
import { AlertController } from '@ionic/angular';
import {HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-shopping-cart-user',
  templateUrl: './shopping-cart-user.page.html',
  styleUrls: ['./shopping-cart-user.page.scss'],
})
export class ShoppingCartUserPage implements OnInit {

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
    //this.loadTablero();
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.getTablero(this.token, this.id).subscribe(data => {
        this.tableros = data;
      });
    });
  }

  loadTablero(){
    
  }


  goEntrenar(tablero_id){
    console.log(tablero_id);
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.playTablero(this.token, tablero_id).subscribe(data => {
        this.tableros = data;
      });
    });
    this.router.navigate(['/tabs-user/index-user'])
  }

  playTablero(token, tablero_id){

    let postData = {
      "tablero_id":tablero_id
    }

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.post(api_url + '/api/play-tablero', postData, {headers: this.headers});
  }

  detenerTablero(tablero_id){
    console.log(tablero_id);
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.offTablero(this.token, tablero_id).subscribe(data => {
        this.tableros = data;
      });
    });
    //this.router.navigate(['/tabs-user/index-user'])
  }

  offTablero(token, tablero_id){

    let postData = {
      "tablero_id":tablero_id
    }

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.post(api_url + '/api/off-tablero', postData, {headers: this.headers});
  }

  goProfileAdmin(){
    this.router.navigate(['/profile-admin'])
  }

  //Listar tableros
  getTablero(token:string, id:string) {

    let postData = {
      "user_id":id
    }

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.post(api_url + '/api/listar-tablero-usuario', postData, {headers: this.headers});
  }

  goCrearTablero(){
    this.router.navigate(['/create-promotion-admin'])
  }

}
