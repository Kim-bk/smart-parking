package com.smartparking.service;

import java.util.List;

import com.smartparking.entity.CustomerEntity;
import com.smartparking.entity.CustomerParkingEntity;

public interface ICustomerParkingService {
	public  List<CustomerParkingEntity> findAll();
	public List<CustomerParkingEntity> findByCustomer(CustomerEntity customer);

}
