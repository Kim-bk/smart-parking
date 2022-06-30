package com.smartparking.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.smartparking.entity.CustomerEntity;
import com.smartparking.entity.CustomerParkingEntity;

public interface CustomerParkingRepository extends MongoRepository<CustomerParkingEntity, String>{
	
	List<CustomerParkingEntity> findByCustomer(CustomerEntity customer);
	

}
