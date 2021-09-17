import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { StorageService, SessionLog } from 'src/app/services/storage.service';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.page.html',
  styleUrls: ['./sign-up.page.scss'],
})
export class SignUpPage implements OnInit {

  constructor(private storageService: StorageService, private router: Router, private http: HttpClient) { }

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  headers: HttpHeaders = new HttpHeaders({
    "Content-Type" : "aplication/json"
  });

  id:string;
  token:string;

  name: string;
  last_name: string;
  email: string;
  phone_number: string;
  address: string;
  born_date: string;
  favorite_flavor: string;
  password: string;
  confirmPassword: string;
  role: string = "jugador"

  respuesta: object;

  ngOnInit() {
  }

  doSignUp(){
    let postData = {
      "name":this.name,
      "last_name":this.last_name,
      "email":this.email,
      "phone_number":this.phone_number,
      "address":this.address,
      "born_date":this.born_date, // Se desea capturar una fecha asi 10/06/2020, por el momento trae una fecha asi 
      "basic_profile":"Futbol",
      "password":this.password,
      "role":this.role
    }

    // console.log(postData);
    let api_url = this.storageService.getApiUrl();

    this.http.post(api_url + '/api/auth/signup', postData, {headers: this.headers})
    .subscribe(data =>{
      // console.log(data);
      this.respuesta = data;

      if(this.respuesta['email']){
        let loginData = {
          "email":this.respuesta['email'],
          "password":this.password
        }
        this.http.post(api_url + '/api/auth/login', loginData, {headers: this.headers})
        .subscribe(data => {
          // console.log(data)
          this.respuesta=data;

          if (this.respuesta['token_type'] == 'Bearer'){

            this.token = this.respuesta['access_token'] + "";
            this.id = this.respuesta['id'] + "";
            this.role = this.respuesta['role'];

            this.saveSession();
            
            if (this.role == "admin")
            {
              this.router.navigate(['/tabs-admin/requested-orders-admin'])
            }
            else if (this.role == "user") 
            {
              this.router.navigate(['/tabs-user/index-user'])
            }
          }

        });
      }
    })
    
  }

  saveSession(){
    this.newSessionLog.email = this.email;
    this.newSessionLog.token = this.token;
    this.newSessionLog.id = this.id;
    this.newSessionLog.role = this.role;

    this.storageService.updateSessionLog(this.newSessionLog).then(sessionLog => {
      this.newSessionLog = <SessionLog>{};
    })
  }

  goLogin(){
    this.router.navigate(['/login'])
  }
}
