import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StorageService, SessionLog } from 'src/app/services/storage.service';
import { ActivatedRoute } from '@angular/router';
import { AlertController } from '@ionic/angular';
import {HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-info-product-admin',
  templateUrl: './info-product-admin.page.html',
  styleUrls: ['./info-product-admin.page.scss'],
})
export class InfoProductAdminPage implements OnInit {

  headers: HttpHeaders;

  id:string;
  email:string;
  password:string;
  user_tablero:object;
  token: string;
  role: string;
  name_user: string;
  usuarios: object;

  new_user: string;
  new_name: string;
  new_description: string;
  new_type: string;
  new_code: string;
  new_status: string;

  tablero;
  tablero2:object;

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  constructor(private http: HttpClient, private router: Router, public alertController: AlertController, private storageService: StorageService, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    let tablero = this.router.getCurrentNavigation().extras
    this.tablero = tablero;
    
    //console.log(this.tablero);
    this.loadPage(tablero);
  }

  loadPage(tablero){
    this.new_name = tablero['device_name'];
    this.new_description = tablero['device_description'];
    this.new_type = tablero['device_type'];
    this.new_code = tablero['device_code'];
    this.new_status = tablero['device_status'];
    this.new_user = tablero['user_id'];
    //console.log(this.router.snapshot.paramMap.get('id'));
    this.loadUser(tablero['user_id'])

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

      let api_url = this.storageService.getApiUrl();

      this.http.get<any>(api_url + '/api/listar-usuarios', {headers: this.headers}).subscribe(data => {
      this.usuarios = data;
      //this.name_user=this.user_tablero['name'];
      //console.log(this.usuarios);
    });
    //console.log(this.usuarios); // should log out 'bar'
    });
  }

  loadUser(user_id){
    //console.log(user_id)
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.getUser(user_id, this.token).subscribe(data => {
        this.user_tablero = data;
        this.name_user=this.user_tablero['name'];
        //console.log(this.user_tablero['name']);
      });
    });
  }

  getUser(user_id, token:string) {

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });
    //console.log(user_id)

    let postData={
      "user_id":"" + user_id
    }

    let api_url = this.storageService.getApiUrl();

    return this.http.post(api_url + '/api/usuario-tablero', postData, {headers: this.headers});
  }

  deleteProduct(){
    console.log('Estas intentando eliminar el producto');
  }

  goEditProduct(){

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

      let postData={
        "new_user":this.new_user,
        "new_name":this.new_name,
        "new_description":this.new_description,
        "new_type":this.new_type,
        "new_code":this.new_code,
        "new_status":this.new_status,
        "tablero_id":this.tablero['id']
      }

      let api_url = this.storageService.getApiUrl();

      this.http.post(api_url + '/api/editar-tablero', postData, {headers: this.headers}).subscribe(data => {
      this.tablero = data;
      //this.name_user=this.user_tablero['name'];
      //console.log(this.tablero);
      this.loadPage(data);
    });

    });
  }

}
