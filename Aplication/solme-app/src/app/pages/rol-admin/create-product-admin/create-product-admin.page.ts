import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { StorageService, SessionLog } from 'src/app/services/storage.service';
import { PhotoService } from '../../../services/photo.service';

@Component({
  selector: 'app-create-product-admin',
  templateUrl: './create-product-admin.page.html',
  styleUrls: ['./create-product-admin.page.scss'],
})
export class CreateProductAdminPage implements OnInit {

  constructor(private storageService: StorageService, private router: Router, private http: HttpClient, public photoService: PhotoService) { }

  sessionLogs: SessionLog[] = [];
  newSessionLog: SessionLog = <SessionLog>{};

  token: string;
  usuario: string;

  headers: HttpHeaders;

  respuesta:object;

  product_type: string;
  product_name: string;
  product_description: string;
  product_price: string;
  product_photo;

  ngOnInit() {
    this.loadSessionLog();
    this.photoService.loadSaved();
  }
  

  goProductsAdmin(){
    this.router.navigate(['tabs-admin/products-admin'])
  }
  // Abrir Camara
  addPhotoToGallery() {
    this.photoService.addNewToGallery();
  }

  AddProduct(){

    console.log('Esta intentando añadir un producto')

    let postData = {
      "product_type": this.product_type,
      "product_name": this.product_name,
      "product_description": this.product_description,
      "product_price": this.product_price,
      "product_photo": this.product_photo,
    }
    console.log(postData);
    
    // this.http.post('http://127.0.0.1:8000/api/create-product-admin', postData, {headers: this.headers})
    // .subscribe(data => {
    //   console.log(data);
    //   this.respuesta = data;
      
    // })

  }

  loadSessionLog(){
    this.storageService.getSessionLog().then(sessionLogs => {
      for (let i of sessionLogs) {
        this.usuario = i.email;
        this.token = i.token;
      
    }
      // console.log(this.usuario);
      // console.log(this.token);

      this.headers = new HttpHeaders({
        "Authorization":"Bearer " + this.token,
        "Content-Type" : "aplication/json"
      });
    });
  }

}
