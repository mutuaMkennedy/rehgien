import React, { Component} from "react";
import styled from 'styled-components';
import proHomeBanner from './static/proHomeBanner.svg';
import cloudsBackground from './static/clouds.jpg';
import groupChat from './static/chat.jpg';
import deals from './static/leads.jpg';
import lead from './static/leadCapture.png';
import chat from './static/chat.png';
import callCenter from './static/callCenter.jpg';
import playstore from './static/google-play-badge.png';
import applestore from './static/apple-store-badge.png';
import logo from './static/logo_pro.png';
import { Icon} from 'semantic-ui-react';

const   HomePage = styled.div`
  width:100%;
  height:100%;
  background-color:#f1f9f1;
`
const  BannerContent = styled.div`
  width:100%;
  height:calc(100vh - 45px);
  background-color:#fff;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
`
const  BannerText = styled.div`
  display: flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  float:left;
  width:60%;
  height:100%;
`
const  BannerHeadings = styled.div`
  padding:10px;
  width:70%;
`
const  BannerTextHeaderSmall = styled.h1`
  color:#555555;
  font-family: 'Ubuntu', sans-serif;
  font-size:15px;
`
const  BannerTextHeader = styled.h1`
  color:#fff;
  font-family: Libre Baskerville, Arial;
  font-size:50px;
`
const  BannerTextSpan = styled.span`
  color:#ffff;
`
const  BannerTextParagraph = styled.p`
  margin-top:20px;
  color:#fff;
  font-size:15px;
  line-height:25px;
  font-family: 'Ubuntu', sans-serif;
`
const  BannerButton= styled.button`
  background:#fb5f3d;
  color:#fff;
  font-family: Lato;
  margin-top:20px;
  width:200px;
  height:45px;
  font-size:15px;
  border:none;
  border-radius:25px;
  :hover{
    opacity:0.8;
    cursor:pointer;
  }
`
const  BannerImgWrapper = styled.div`
  display: flex;
  justify-content:center;
  align-items:center;
  float:right;
  width:40%;
  height:100%;
  @media (max-width: 786px){
    display:none;
  }
`
const  HomeSection = styled.div`
  width:100%;
  height:250px;
  display: flex;
  justify-content:center;
  align-items:center;
  flex-direction:column;
  background-color:#fff;
`
const  HomeHeader = styled.h1`
  color:#000;
  font-family: Libre Baskerville, Arial;
  font-size:30px;
  text-align:center;
  line-height:30px;
`
const  HomeParagraph = styled.p`
  color:#000;
  width:600px;
  font-family:'Ubuntu', sans-serif;
  font-size:15px;
  margin-top:20px;
  line-height:26px;
  text-align:center;
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
  /* @media (max-width: 786px){
    width:100%;
  } */
`
const  PageSection = styled.div`
  width:100%;
  height:650px;
  display: flex;
  justify-content:center;
  align-items:flex-end;
  flex-direction:column;
  background-color:#fff;
  /* @media (max-width: 786px){
    flex-direction:column;
    align-items:center;
  } */
`
const  PageSectionContent = styled.div`
  width:100%;
  height:500px;
  display: flex;
  justify-content:space-between;
  align-items:center;
  /* @media (max-width: 786px){
    flex-direction:column;
    justify-content:center;
    height:auto;
  } */
`
const PageSectionText = styled.div`
  width:40%;
  height:100%;
  margin-top:150px;
  margin-left:150px;
  /* @media (max-width: 786px){
    margin-top:0;
    margin-left:0;
    width:100%;
    padding:10px;
  } */
`
const  PageSectionHeader = styled.h1`
  color:#000;
  font-family: Libre Baskerville, Arial;
  font-size:30px;
  text-align:start;
`
const  PageSectionParagraph = styled.p`
  width:400px;
  margin-top:20px;
  color:#000;
  font-size:15px;
  line-height:20px;
  font-family: 'Ubuntu', sans-serif;
`
const  PageSectionParagraphSpan = styled.span`
    display:flex;
    align-items:baseline;
    justify-content:start;
`
const  PageSectionButton= styled.button`
  background:blue;
  color:#fff;
  font-family: Lato;
  margin-top:20px;
  width:200px;
  height:45px;
  font-size:15px;
  border:none;
  border-radius:25px;
  :hover{
    opacity:0.8;
    cursor:pointer;
  }
`
const PageSectionImage = styled.div`
  width:100%;
  height:100%;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
  /* border-radius:50%; */
  border-top-left-radius:10px;
  /* border-bottom-right-radius:50%; */
  border-bottom-left-radius:10px;
`
const PageSectionSmallImage = styled.div`
  width:255px;
  height:100%;
  background-position: bottom !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
  border-radius:10px;
  position:relative;
  bottom:90%;
  right:50px;
  /* margin-left:auto; */
  margin-right:auto;
  background-color:#fff;
`
const PageSectionImageBox = styled.div`
  width:60%;
  height:100%;
  border-radius:10px;
  position:relative;
`
const  PageSection1 = styled.div`
  width:100%;
  height:500px;
  margin-top:150px;
  display: flex;
  justify-content:center;
  align-items:flex-start;
  flex-direction:column;
  background-color:#f1f9f1;
`
const PageSectionImage1 = styled.div`
  width:100%;
  height:100%;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
  border-top-right-radius:10px;
  border-bottom-right-radius:10px;
  /* border-radius:50%; */
`
const PageSectionSmallImage1 = styled.div`
  width:50%;
  height:100%;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: contain !important;
  border-radius:10px;
  position:relative;
  bottom:90%;
  left:15px;
  /* margin-left:auto; */
  margin-left:auto;
  background-color:#fff;
`
const PageSectionText1 = styled.div`
  width:40%;
  height:100%;
  margin-top:150px;
  margin-left:100px;
`
const  PageSection2 = styled.div`
  width:100%;
  height:500px;
  display: flex;
  justify-content:center;
  align-items:center;
  flex-direction:column;
  background:#000;
  color:#ffff;
`
const  PageSectionHeader2 = styled.h1`
  color:#fff;
  font-family: Libre Baskerville, Arial;
  font-size:30px;
  text-align:start;
`
const  PageSectionContent2 = styled.div`
  padding:10px;
  width:650px;
  height:500px;
  display: flex;
  flex-direction:column;
  justify-content:center;
  align-items:center;
`
const  PageSectionParagraph2 = styled.p`
  width:650px;
  margin-top:20px;
  color:#fff;
  font-size:15px;
  line-height:20px;
  font-family: 'Ubuntu', sans-serif;
`
const  PageSectionButton2= styled.button`
  background:blue;
  color:#fff;
  font-family: Lato;
  margin-top:20px;
  width:200px;
  height:45px;
  font-size:15px;
  border:none;
  border-radius:25px;
  :hover{
    opacity:0.8;
    cursor:pointer;
  }
`
const  PageSection3 = styled.div`
  width:100%;
  height:500px;
  margin-top:200px;
  display: flex;
  justify-content:center;
  align-items:center;
  flex-direction:column;
  background-color:#003188;
  color:#fff;
`
const  PageLinks = styled.div`
  width:100%;
  height:600px;
  display: flex;
  justify-content:center;
  align-items:center;
  background-color:#fff;
  color:#000;
`
const  PageLinksItems = styled.div`
  width:100%;
  height:auto;
  display: flex;
  justify-content:flex-start;
`
const  PageLinksContent = styled.div`
  width:100%;
  height:auto;
  display: flex;
  flex-direction:column;
  justify-content:flex-start;
  align-items:center;
`
const PageLinksImage = styled.div`
  width:200px;
  height:200px;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: cover !important;
  border-radius:50%;
`
const PageLinksText = styled.div`
  width:40%;
  height:auto;
  margin-top:50px;
`
const   PageLinksHeader = styled.h1`
  color:#000;
  font-family: Libre Baskerville,Arial;
  font-size:23px;
  text-align:center;
`
const  PageLinksParagraph = styled.p`
  width:100%;
  text-align:center;
  margin-top:20px;
  color:#000;
  font-size:15px;
  line-height:20px;
  font-family: 'Ubuntu', sans-serif;
`
const PageLinksImageBox = styled.div`
  width:50%;
  height:auto;
  display:flex;
  justify-content:space-around;
  align-items:center;
`
const  PageFooter = styled.div`
  width:100%;
  height:200px;
  display: flex;
  justify-content:center;
  align-items:center;
  background-color:#fff;
  color:#000;
  border-top:1px solid #d1d1d1;
`
const  PageFooterGroupLeft = styled.div`
  width:30%;
  height:100%;
  margin-top:50px;
  display: flex;
  justify-content:flex-start;
  flex-direction:column;
  align-items:center;
  background-color:#fff;
  color:#000;
`
const  PageFooterGroupRight = styled.div`
  width:70%;
  height:100%;
  margin-top:50px;
  display: flex;
  justify-content:flex-end;
  align-items:center;
  background-color:#fff;
  color:#000;
`
const  PageFooterLogo = styled.div`
  width:200px;
  height:60px;
  background-position: center !important;
  background-repeat: no-repeat !important;
  background-size: contain !important;
`
const  PageNavLinkWrap = styled.div`
  width:20%;
  height:100%;
  display:flex;
  flex-direction:column;
  justify-content:flex-start;
`
const  PageNavLinkHeader = styled.h1`
  font-family:Arial;
  font-size:13px;
  text-transform: uppercase;
  color:#757575;
`
const  PageNavLinkItem = styled.li`
  font-family:Noto Sans Jp,Arial;
  font-size:12px;
  text-transform: uppercase;
  list-style: none;
`
const  PageSmallFooter = styled.div`
  width:100%;
  height:50px;
  display: flex;
  justify-content:center;
  align-items:center;
  background-color:#fff;
  color:#000;
  border-top:1px solid #d1d1d1;
`


class Home extends Component {

  render() {
    return (
      <HomePage>
          <BannerContent style={{'backgroundImage': `linear-gradient( rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2) ),url(${cloudsBackground})`}}>
              <BannerText>
                <BannerHeadings>
                  <BannerTextHeaderSmall>
                    <BannerTextHeader> Get More Working<br/><BannerTextSpan> With Us.</BannerTextSpan></BannerTextHeader>
                    Tailored Solutions for Real Estate Proffesionals.
                  </BannerTextHeaderSmall>
                  <BannerTextParagraph>
                    Built for Proffesionals by Proffesionals.
                    <br/>
                    This is the place to generate more deals and leads.
                    Connect and grow with thousands of agents nationwide.
                  </BannerTextParagraph>
                  <BannerButton>
                  <a href='/pro/auth/login' style={{'color':'#fff'}}>
                    Get Started
                  </a>
                  </BannerButton>
                </BannerHeadings>
              </BannerText>
              <BannerImgWrapper>
                    <img src={proHomeBanner} style={{'width':'100%','objectFit':'center'}}/>
              </BannerImgWrapper>
          </BannerContent>

          <HomeSection>
            <HomeHeader>
              What We Offer
            </HomeHeader>
            <div style={{'width':'100px', 'height':'10px', 'background':'#fb5f3d', 'borderRadius':'25px'}}/>
            <HomeParagraph>Gain more with us. We are continually building new features to
            address various painpoints Real Estate Proffesionals face.
             </HomeParagraph>
          </HomeSection>

          <PageSection>
            <PageSectionContent>
                <PageSectionText>
                    <div style={{'width':'100px', 'height':'25px', 'background':'#fb5f3d', 'borderRadius':'25px'}}/>
                    <PageSectionHeader>Save Time, Get Qualified Leads</PageSectionHeader>
                    <PageSectionParagraph>
                    Getting motivated clients is hard. We make it easy with our pre-qualified leads.
                    <br/>
                    <br/>
                     You get leads in two ways:
                    <br/>
                    <br/>
                    <PageSectionParagraphSpan><Icon name='check circle outline'/> From clients using our platform.</PageSectionParagraphSpan>
                    <br/>
                    <PageSectionParagraphSpan><Icon name='check circle outline'/> From other agents in the network.</PageSectionParagraphSpan>
                    <br/>
                    Accept leads in real time.
                    </PageSectionParagraph>
                    <a href='/pro/markets/leads/property_requests' style={{'color':'#fff'}}><PageSectionButton>View Requests</PageSectionButton></a>
                </PageSectionText>
                <PageSectionImageBox>
                  <PageSectionImage  style={{'backgroundImage': `linear-gradient( rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.1) ),url(${deals})`}}>

                  </PageSectionImage>
                  <PageSectionSmallImage  style={{'backgroundImage': `url(${lead})`,'display':'block'}}/>
                </PageSectionImageBox>
            </PageSectionContent>
          </PageSection>
          <PageSection1>
            <PageSectionContent>
                <PageSectionImageBox>
                  <PageSectionImage1  style={{'backgroundImage': `linear-gradient( rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.2) ),url(${groupChat})`}}>

                </PageSectionImage1>
                  <PageSectionSmallImage1 style={{'backgroundImage': `url(${chat})`,'display':'block'}}/>
                </PageSectionImageBox>
                <PageSectionText1>
                    <div style={{'width':'100px', 'height':'25px', 'background':'#fb5f3d', 'borderRadius':'25px'}}/>
                    <PageSectionHeader>Engage With Other <br/>Agents.</PageSectionHeader>
                    <PageSectionParagraph>
                    Experience seemless communication with other members on rehgien messaging.
                    <br/>
                    <br/>
                    <PageSectionParagraphSpan><Icon name='check circle outline'/> Share Files.</PageSectionParagraphSpan>
                    <br/>
                    <PageSectionParagraphSpan><Icon name='check circle outline'/> Start Threads.</PageSectionParagraphSpan>
                    <br/>
                    <PageSectionParagraphSpan><Icon name='check circle outline'/> Audio and Voice Calls in a click.</PageSectionParagraphSpan>
                    <br/>
                    <PageSectionParagraphSpan><Icon name='check circle outline'/> Collaborate With Other Agents.</PageSectionParagraphSpan>
                    <br/>
                    Everyone is here! Meet new people and grow your
                    network.
                    </PageSectionParagraph>
                    <a href='/pro/messaging' style={{'color':'#fff'}}><PageSectionButton>Start Messaging</PageSectionButton></a>
                </PageSectionText1>
            </PageSectionContent>
          </PageSection1>

          <PageSection3>
            <PageSectionContent2 style={{'position':'relative'}}>
                <div style={{'width':'100px', 'height':'25px', 'background':'#fb5f3d', 'borderRadius':'25px'}}/>
                <PageSectionHeader2 style={{'textAlign':'center'}}>Real Estate Proffesionals.</PageSectionHeader2>
                <PageSectionParagraph2 style={{'textAlign':'center'}}>
                  We put our customers first and immensely value your feedback.
                  <br/>
                  Join our Insider Programme and be the first to access new features.
                  Help us build great solutions that improve your life as a proffesional.
                </PageSectionParagraph2>
                <div style={{'display':'flex', 'justifyContent':'space-around', 'alignItems':'center', 'width':'500px'}}>
                  <PageSectionButton2>Join Insider Programme</PageSectionButton2>
                </div>
            </PageSectionContent2>
          </PageSection3>
          <PageSection2>
            <PageSectionContent2 style={{'position':'relative'}}>
                <div style={{'width':'100px', 'height':'25px', 'background':'#fb5f3d', 'borderRadius':'25px'}}/>
                <PageSectionHeader2 style={{'textAlign':'center'}}>Service Providers Partnership Programme.</PageSectionHeader2>
                <PageSectionParagraph2 style={{'textAlign':'center'}}>
                  Real estate is one of the most service diverse industries.
                  We are open to partnering with various service providers ranging from utility service providers,
                  designers, movers etc. to offer more value to our clients and members as we help you grow your business.
                  Be a part of the Rehgien Community, grow your business with us.
                </PageSectionParagraph2>
                <div style={{'display':'flex', 'justifyContent':'space-around', 'alignItems':'center', 'width':'500px'}}>
                  <PageSectionButton2>Become a Partner</PageSectionButton2>
                  <PageSectionButton2>Learn More</PageSectionButton2>
                </div>
            </PageSectionContent2>
          </PageSection2>
          <PageLinks>
            <PageLinksItems>
              <PageLinksContent>
                <PageLinksImage style={{'backgroundImage': `url(${groupChat})`}}/>
                <PageLinksText>
                  <PageLinksHeader>
                    Never miss a thing
                  </PageLinksHeader>
                  <PageLinksParagraph>
                    Experience all of this and more on our app. Stay in sync all the time.
                  </PageLinksParagraph>
                </PageLinksText>
                <PageLinksImageBox>
                  <a href='#' style={{'marginTop':'0px','width':'150px','height':'150px'}}>
                    <img src={applestore} style={{'width':'100%','height':'100%'}}/>
                  </a>
                  <a href='#' style={{'marginTop':'0px','width':'150px','height':'150px'}}>
                    <img src={playstore} style={{'width':'100%','height':'100%'}}/>
                  </a>
                </PageLinksImageBox>
              </PageLinksContent>
              <PageLinksContent>
                  <PageLinksImage style={{'backgroundImage': `url(${callCenter})`}}/>
                  <PageLinksText>
                    <PageLinksHeader>
                      Talk to us
                    </PageLinksHeader>
                    <PageLinksParagraph>
                      Have something to share? Reach us directly.
                    </PageLinksParagraph>
                  </PageLinksText>
              </PageLinksContent>
            </PageLinksItems>
          </PageLinks>
          <PageFooter>
            <PageFooterGroupLeft>
              <PageFooterLogo style={{'backgroundImage': `url(${logo})`}}/>
            </PageFooterGroupLeft>
            <PageFooterGroupRight>
            <PageNavLinkWrap>
              <PageNavLinkHeader>Company</PageNavLinkHeader>
              <PageNavLinkItem><a href='' style={{'color': '#757575'}}>About Us</a></PageNavLinkItem>
              <PageNavLinkItem><a href='' style={{ 'color': '#757575'}}>Contact Us</a></PageNavLinkItem>
              <PageNavLinkItem><a href='' style={{ 'color': '#757575'}}>Privacy Policy</a></PageNavLinkItem>
              <PageNavLinkItem><a href='' style={{ 'color': '#757575'}}>Terms & Conditions</a></PageNavLinkItem>
            </PageNavLinkWrap>
            <PageNavLinkWrap>
              <PageNavLinkHeader>Follow Us</PageNavLinkHeader>
              <PageNavLinkItem><a href='' style={{'color': '#757575'}}>Facebook</a></PageNavLinkItem>
              <PageNavLinkItem><a href='' style={{ 'color': '#757575'}}>Twitter</a></PageNavLinkItem>
              <PageNavLinkItem><a href='' style={{ 'color': '#757575'}}>Linkedin</a></PageNavLinkItem>
            </PageNavLinkWrap>
            </PageFooterGroupRight>
          </PageFooter>
          <PageSmallFooter>Copyright 2020</PageSmallFooter>
      </HomePage>
    );
  }
}

export default Home;
