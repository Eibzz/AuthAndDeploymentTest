gURL = "https://deploy-the-cookies.herokuapp.com/";

var MakeHTTPRequest = function(action, callback) {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if(request.readyState == XMLHttpRequest.DONE) {
			if(request.status < 400 && request.status >= 200) {
				callback(request);
			}
			else {
				if(request.responseText){
					alert(request.responseText);
				}
			}
		}
	}
	action(request);
};

/// button onclick events and actions ///
document.getElementById("input-register").onclick = function() {
	MakeHTTPRequest(actionRegister, function(request) {
		alert("Successfully registered! You may now login.");
		var email = document.getElementById("register-email");
		var pass = document.getElementById("register-password");
		var first = document.getElementById("register-firstname");
		var last = document.getElementById("register-lastname");
		email.value = "";
		pass.value = "";
		first.value = "";
		last.value = "";
	});
}
var actionRegister = function(request) {
	var email = document.getElementById("register-email");
	var pass = document.getElementById("register-password");
	var first = document.getElementById("register-firstname");
	var last = document.getElementById("register-lastname");
	request.open("POST", gURL+"users");
	request.withCredentials = true;
	request.setRequestHeader("content-type", "application/x-www-form-urlencoded");
	request.send("email="+email.value+"&encpass="+pass.value+"&firstname="+first.value+"&lastname="+last.value);
}

document.getElementById("input-login").onclick = function() {
	MakeHTTPRequest(actionLogin, function(request) {
		var reg = document.getElementById("input-section-register");
		var log = document.getElementById("input-section-login");
		var par = document.getElementById("left-column")
		par.removeChild(reg);
		par.removeChild(log);
		document.getElementById("input-section-message").style.visibility = "visible";
		MakeHTTPRequest(getMessages, function(request2) {
			showMessages(request2);
		});
	});
}
var actionLogin = function(request) {
	var email = document.getElementById("login-email");
	var pass = document.getElementById("login-password");
	request.open("POST", gURL+"session");
	request.withCredentials = true;
	request.setRequestHeader("content-type", "application/x-www-form-urlencoded");
	request.send("email="+email.value+"&encpass="+pass.value);
}

document.getElementById("send-message").onclick = function() {
	var msg = document.getElementById("message");
	if(msg.value) {
		MakeHTTPRequest(postMessage, function(request) {
			MakeHTTPRequest(getMessages, function(request2) {
				msg.value = "";
				showMessages(request2);		
			});
		});
	}
	else {
		alert("Message cannot be blank.");
	}
}

var postMessage = function (request) {
	var message = document.getElementById("message");
	request.open("POST", gURL+"messages");
	request.withCredentials = true;
	request.setRequestHeader("content-type", "application/x-www-form-urlencoded");
	var now = new Date().toLocaleString();
	request.send("message="+message.value+"&timestamp="+now);	
};

var getMessages = function(request) {
	request.open("GET", gURL+"messages");
	request.withCredentials = true;
	request.send();
};

var showMessages = function(request) {
	var jsonmessages = JSON.parse(request.responseText);
	console.log(jsonmessages);
	
	var messageList = document.getElementById("message-list");
	while(messageList.hasChildNodes()){
		messageList.removeChild(messageList.firstChild);
	}
	
	for(i = 0; i<jsonmessages.length; i++) {
		var messageItem = document.createElement("li");
		messageItem.className = "message-item";
		messageItem.innerHTML = 
			"(" + jsonmessages[i]["timestamp"] + ") " +
			jsonmessages[i]["sender"] + " | " +
			jsonmessages[i]["message"];
		messageList.appendChild(messageItem);
	}
};

//Getting string of current local time
var now = new Date().toLocaleString();
console.log(now);

MakeHTTPRequest(getMessages, function(request) {
	if(request.responseText != "Not logged in."){
		var reg = document.getElementById("input-section-register");
		var log = document.getElementById("input-section-login");
		var par = document.getElementById("left-column")
		par.removeChild(reg);
		par.removeChild(log);
		document.getElementById("input-section-message").style.visibility = "visible";
		showMessages(request);
	}
});