package com.smartparking.repository;

import java.util.List;

import org.springframework.data.mongodb.repository.MongoRepository;

import com.smartparking.entity.CustomerEntity;


public interface CustomerRepository extends MongoRepository<CustomerEntity, String>{
	List<CustomerEntity> findByCustomerCard(String customerCard);
	List<CustomerEntity> findByEmail(String email);

}
