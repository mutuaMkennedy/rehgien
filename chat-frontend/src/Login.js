import React, { Component } from "react";
import axios from "axios";
import styled from 'styled-components';
import base from './baseAddress.js';

//Login Page styled css components
const StLoginRoot = styled.div`
  display:flex;
  height:100vh;
  position:absolute;
  background:#fff;
  top:0;
  @media (max-width: 786px) {
    flex-direction:column;
  }
`

const StLoginCWrapper = styled.div`
  margin-top:10%;
  width:50%;
  display:flex;
  /* justify-content:center; */
  align-items:center;
  flex-direction:column;
  @media (max-width: 786px) {
    width:100%;
  }
`

const StLoginBanner = styled.div`
  width:50%;
  background-image:linear-gradient(rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1)),url('https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1500&q=80');
  background-position:center;
  background-repeat: no-repeat;
  background-size: cover;
  border-radius:10px;
  margin:5px;
  @media (max-width: 786px) {
    display:none;
  }
`

const LoginLogo = styled.div`
  width:65px;
  height:65px;
  background:url('${base}/static/img/logo-fav.png');
  background-position:center;
  background-size:contain;
  background-repeat: no-repeat !important;
`

const StLoginBnTitleWrp = styled.div`
  width:auto;
  height:auto;
  margin-top:40%;
  transform: translate(0,-40%);
`

const StLoginBnTitle = styled.h1`
  color:#ffffff;
  text-align:center;
  font-size:45px;
  font-family:'MuseoModerno',Noto Sans Jp,Arial;
`

const StLoginBnParagraph = styled.p`
  color:#ffffff;
  text-align:center;
  font-size:15px;
  font-family:'MuseoModerno',Noto Sans Jp,Arial;
`

const StLoginCard = styled.div`
  /* margin-top:10%; */
  /* margin-bottom:auto; */
  display:flex;
  flex-direction:column;
  @media (max-width: 786px) {
    width:90%;
  }
`

const Title = styled.h1`
  font-size:25px;
  font-family:Noto Sans Jp, Roboto, Arial;
  font-weight:100;

`

const LgInputWrapper = styled.div`
  font-size:20px;
  font-family:Not Sans Jp, Roboto, Arial;
  font-weight:bold;
  margin-top:5px;
  display:flex;
  @media (max-width: 786px) {
    flex-direction:column;
  }

`

const Input = styled.input`
  width:250px;
  height:35px;
  border:1px solid #dddddd;
  margin-right:5px;
  margin-bottom:10px;
  font-size:14px;
  ::placeholder {
    font-family:Roboto, Arial;
    font-size:14px;
  }
  @media (max-width: 786px) {
    width:100%;
  }

`

const Button = styled.button`
  width:100px;
  height:40px;
  border:1px solid #dddddd;
  border-radius:5px;
  margin-top:10px;
  background-color:#ffffff;
  color:#13031b;
  :hover{
      border:2px solid #13031b;
      cursor:pointer;
  }

`
const LoginInfWrapper = styled.div`
  width:100%;
  heigh:auto;
  border-radius:5px;
  background-color:#141414;
  margin-top:50px;
  padding:10px;

`
const LoginInfWrapperParagraph = styled.p`
  color:#ffffff;
  font-family:Roboto, Arial;
  font-size:12px;
  font-weight:lighter;
  text-align:center;
`


//Login component
class Login extends Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: false,
      username: "",
      password: "",
      u_errors: '',
      p_error:'',
      auth_error:''
    };

    this.initStream = this.initStream.bind(this);
  }

  async initStream() {
    await this.setState({
      loading: true,
    });


    if(this.state.username !==''){
      if(this.state.password !==''){
        try {
            const authorization = await axios({
              method: "POST",
              url: `${base}/apis/rest-auth/login/ `,
              data: {
                username:this.state.username,
                password:this.state.password,
                user_id:this.state.user_id,
                user_name:this.state.user_name,
                user_avatar:this.state.user_avatar,
              },
              config: {
                headers: { "Content-Type": "application/json" }
              }
            });

            localStorage.setItem("token", authorization.data.stream_token);
            localStorage.setItem("auth_token", authorization.data.auth_token);
            localStorage.setItem("user_id", authorization.data.user_id);
            localStorage.setItem("user_name", authorization.data.user_name);
            localStorage.setItem("user_avatar", authorization.data.user_avatar);

            await this.setState({
              loading: false,
              p_errors:'',
              u_errors:'',
              auth_error:''
            });

            this.props.history.go("/pro/home");

        } catch (e) {
          this.setState({
            auth_error:'Login failed. Username or password entered is not correct',
          });
        }
      }else{
        this.setState({
          p_errors: 'Enter password',
        });
      }


      } else {
        this.setState({
          u_errors: 'Enter username',
        });
      }

  }

  handleChange = e => {
    this.setState({
      [e.target.name]: e.target.value
    });
  };

  render() {
    return (
        <StLoginRoot>
            <StLoginCWrapper>
                  <LoginLogo/>
                  <StLoginCard>
                    <Title>Login</Title>
                      <form>
                      <LgInputWrapper>
                          <div style={{"display":"flex", "flexDirection":'column'}}>
                            <Input
                              type="text"
                              placeholder="username"
                              name="username"
                              onChange={e => this.handleChange(e)}
                            />
                            <span style={{"color": "#db2828","fontFamily": "Arial","fontSize": "10px",}}>{this.state.u_errors}</span>
                          </div>
                          <div style={{"display":"flex", "flexDirection":'column'}}>
                              <Input
                                type="password"
                                placeholder="Password"
                                name="password"
                                onChange={e => this.handleChange(e)}
                              />
                              <span style={{"color": "#db2828","fontFamily": "Arial","fontSize": "10px"}}>{this.state.p_errors}</span>
                          </div>
                      </LgInputWrapper>
                      <span style={{"color": "#db2828","fontFamily": "Arial","fontSize": "10px",}}>{this.state.auth_error}</span>
                      </form>
                      <Button onClick={this.initStream}>Login</Button>
                      <LoginInfWrapper>
                        <LoginInfWrapperParagraph>
                          This part of Rehgien is exclusive to verified pro accounts. Other users visit<a href={base + '/'}> here.</a>
                        </LoginInfWrapperParagraph>
                        <LoginInfWrapperParagraph>
                          If you are a pro and don't have an account please <a href={base + '/accounts/signup/'}>signup</a> first.

                        </LoginInfWrapperParagraph>
                      </LoginInfWrapper>
                  </StLoginCard>
              </StLoginCWrapper>
            <StLoginBanner>
              <StLoginBnTitleWrp>
                  <StLoginBnTitle>Join The</StLoginBnTitle>
                  <StLoginBnTitle>Growing Community</StLoginBnTitle>
                  <StLoginBnParagraph>
                  Join a comunity of Real Estate Proffesionals on Rehgien.
                  Experience a collection of exlusive features tailored for proffesionals.
                  </StLoginBnParagraph>
              </StLoginBnTitleWrp>
            </StLoginBanner>
        </StLoginRoot>
    );
  }
}

export default Login;
