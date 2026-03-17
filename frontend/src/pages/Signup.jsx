import AuthForm from '../components/AuthForm';
import { signup } from '../services/api';

export default function Signup() {
  return (
    <AuthForm
      mode="signup"
      onSubmit={({ username, email, password }) => signup(username, email, password)}
    />
  );
}
