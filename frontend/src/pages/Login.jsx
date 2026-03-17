import AuthForm from '../components/AuthForm';
import { login } from '../services/api';

export default function Login() {
  return (
    <AuthForm
      mode="login"
      onSubmit={({ username, password }) => login(username, password)}
    />
  );
}
