import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-toppings-admin',
  templateUrl: './toppings-admin.page.html',
  styleUrls: ['./toppings-admin.page.scss'],
})
export class ToppingsAdminPage implements OnInit {

  constructor(private router: Router) { }

  ngOnInit() {
  }

  goCreateTopping(){
    this.router.navigate(['/create-topping-admin'])
  }

  goInfoTopping(){
    this.router.navigate(['/info-topping-admin'])
  }

}
