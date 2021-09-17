import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StorageService, SessionLog } from 'src/app/services/storage.service';
import { ActivatedRoute } from '@angular/router';
import { AlertController } from '@ionic/angular';
import {HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-index-user',
  templateUrl: './index-user.page.html',
  styleUrls: ['./index-user.page.scss'],
})
export class IndexUserPage implements OnInit {

  headers: HttpHeaders;

  id:string;
  email:string;
  password:string;
  tablero:object;
  token: string;
  role: string;
  deporte = "Futbol"

  users_aproved:object;
  users_rejected:object;
  users_waiting:object;

  respuesta

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  constructor(private http: HttpClient, private router: Router, public alertController: AlertController, private storageService: StorageService, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
  }

  goAnotacion(resultado){
    //console.log(resultado)

    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }

      this.getTablero(this.token, this.id).subscribe(data => {
        this.tablero = data[0];

        if ((this.tablero['user_id'] == this.id) && (this.tablero['status'] == "Encendido")){
          this.postResultado(this.id, this.tablero['id'], resultado, this.deporte, this.token).subscribe(data => {
            this.respuesta = data;
            //console.log(this.respuesta);
        })
      }
      });
    });
  }

  postResultado(user_id, tablero_id, resultado, deporte, token){
    let postData = {
      "user_id":user_id,
      "device_id":tablero_id,
      "resultado":resultado,
      "deporte":deporte
    }

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.post(api_url + '/api/anotacion-fracaso', postData, {headers: this.headers});
  }

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


  goShoppingCart(){
    this.router.navigate(['/shopping-cart-user'])
  }

}
