import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-products-admin',
  templateUrl: './products-admin.page.html',
  styleUrls: ['./products-admin.page.scss'],
})
export class ProductsAdminPage implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

  goCreateProduct(){
    this.router.navigate(['/create-product-admin'])
  }

  goInfoProduct(){
    this.router.navigate(['/info-product-admin'])
  }
  goProfileAdmin(){
    this.router.navigate(['/profile-admin'])
  }
}
