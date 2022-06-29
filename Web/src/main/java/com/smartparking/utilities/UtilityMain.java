package com.smartparking.utilities;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import com.smartparking.service.impl.CustomerService;

@Component
public class UtilityMain {

	
	@Autowired
	private CustomerService service;
	
	public String createIDCustomer() {
		int leng = service.findAll().size();
		String st = "KH" + leng;
		return st;
	}
}
