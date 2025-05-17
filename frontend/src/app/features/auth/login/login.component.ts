import { Component, OnInit } from '@angular/core';
import {
  FormBuilder,
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { PasswordModule } from 'primeng/password';
import { ToastModule } from 'primeng/toast';
import { LoginFormGroup } from '../../../core/models/ui/login/LoginFormGroup';
import { AuthService } from '../../../core/services/auth.service';
import { Router } from '@angular/router';
import { LoginForm } from '../../../core/models/ui/login/LoginForm';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-login',
  imports: [
    FormsModule,
    ReactiveFormsModule,
    InputTextModule,
    PasswordModule,
    ToastModule,
    ButtonModule,
  ],
  providers: [MessageService],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent implements OnInit {
  loginFormGroup!: FormGroup<LoginFormGroup>;

  isLoading: boolean = false;

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router,
    private messageService: MessageService
  ) {}

  ngOnInit() {
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }
    this.resetLoginFormGroup();
  }

  resetLoginFormGroup() {
    this.loginFormGroup = this.formBuilder.group<LoginFormGroup>({
      username: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required],
      }),
      password: new FormControl('', {
        nonNullable: true,
        validators: [Validators.required],
      }),
    });
  }

  onLoginSubmit() {
    const loginData: LoginForm = this.loginFormGroup.getRawValue();

    this.isLoading = true;
    this.authService.login(loginData).subscribe({
      next: (res) => {
        this.isLoading = false;
        this.authService.setToken(res.access_token);
        this.router.navigate(['/dashboard']);
      },
      error: (err) => {
        this.isLoading = false;
        this.messageService.add({
          severity: 'error',
          summary: 'Error',
          detail: 'Invalid Credentials',
        });
      },
    });
  }
}
