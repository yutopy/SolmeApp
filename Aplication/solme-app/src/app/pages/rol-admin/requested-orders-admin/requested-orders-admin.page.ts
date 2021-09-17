import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StorageService, SessionLog } from 'src/app/services/storage.service';
import { ActivatedRoute } from '@angular/router';
import { AlertController } from '@ionic/angular';
import {HttpClient, HttpHeaders } from '@angular/common/http';



@Component({
  selector: 'app-requested-orders-admin',
  templateUrl: './requested-orders-admin.page.html',
  styleUrls: ['./requested-orders-admin.page.scss'],
})
export class RequestedOrdersAdminPage implements OnInit {

  headers: HttpHeaders;

  id:string;
  email:string;
  password:string;
  respuesta:object;
  token: string;
  role: string;

  users_aproved:object;
  users_rejected:object;
  users_waiting:object;

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  constructor(private http: HttpClient, private router: Router, public alertController: AlertController, private storageService: StorageService, private activatedRoute: ActivatedRoute) { }

  ngOnInit() {
    this.cargarPagina();
  }

  infoUser(user){

    this.presentAlert(user);

  }

  checkUser(user_id){

    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        //this.role = i.role;
      }
  
      this.aceptarUsuario(user_id, this.token).subscribe(data => {
        this.respuesta = data;
        //this.presentAlert(this.respuesta);
        
      });
    });
    this.cargarPagina();

  }

  rechazarUser(user_id){

    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        this.role = i.role;
      }
  
      this.rechazarUsuario(user_id, this.token).subscribe(data => {
        this.respuesta = data;
        //console.log(this.respuesta);
        
      });
    });
    this.cargarPagina();

  }

  cargarPagina(){
    //this.role = this.activatedRoute.snapshot.paramMap.get('role');
    this.role="jugador";

    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.id = i.id;
        this.token = i.token;
        //this.role = i.role;
      }
  
      this.getVerificarUsuarios(this.role, this.token).subscribe(data => {
        this.respuesta = data;
        this.users_aproved = this.respuesta['users_aproved'];
        this.users_rejected = this.respuesta['users_rejected'];
        this.users_waiting = this.respuesta['users_waiting'];

        console.log(this.respuesta);
        
      });
    });
  }

  async presentAlert(user) {
    console.log(user);
    const alert = await this.alertController.create({
      cssClass: 'my-custom-class',
      header: 'Información de usuario',
      subHeader: user.name,
      message: 'Apellido: ' + user.last_name + '<br> E-mail: ' + user.email + '<br> Teléfono: ' + user.phone_number + '<br> Identificación: ' + user.identification + '<br> Fecha nacimiento: ' + user.born_date,
      buttons: ['OK']
    });

    await alert.present();
  }

  goProfileAdmin(){
    this.router.navigate(['/profile-admin'])
  }

  //Verificacion de usuarios
  getValidarUsuarios(token:string) {

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.get<any>(api_url + '/api/validar-usuarios', {headers: this.headers});
  }

  getVerificarUsuarios(role:string, token:string) {

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.get<any>(api_url + '/api/verificar-usuarios?role=' + role, {headers: this.headers});
  }

  rechazarUsuario(user_id:string, token:string){
    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let postData = {
      "user_id":user_id
    }

    let api_url = this.storageService.getApiUrl();

    return this.http.post(api_url + '/api/rechazar-usuario', postData, {headers: this.headers});
  }

  aceptarUsuario(user_id:string, token:string){
    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let postData = {
      "user_id":user_id
    }

    let api_url = this.storageService.getApiUrl();

    return this.http.post(api_url + '/api/aceptar-usuario', postData, {headers: this.headers});

  }

  //Verificacion de solicitudes de entrada

  getCargarSolicitudes(role:string, token:string) {

    this.headers = new HttpHeaders({
      "Authorization":"Bearer " + token,
      "Content-Type" : "aplication/json"
    });

    let api_url = this.storageService.getApiUrl();

    return this.http.get<any>(api_url + '/api/cargar-solicitudes', {headers: this.headers});
  }

}
